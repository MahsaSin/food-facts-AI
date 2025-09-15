import math
from typing import Dict, List, Optional, Tuple

import pandas as pd
from datasets import load_dataset


class NutritionEvaluator:
    def __init__(
        self, metrics: Optional[List[str]] = None, join_key: str = "meal_description"
    ):
        self.metrics = metrics or ["carb", "fat", "energy", "protein"]
        self.join_key = join_key

    @staticmethod
    def _to_numeric(df: pd.DataFrame, cols: List[str]) -> pd.DataFrame:
        for c in cols:
            df[c] = pd.to_numeric(df[c], errors="coerce")
        return df

    def evaluate(
        self, ref_df: pd.DataFrame, pred_df: pd.DataFrame
    ) -> Tuple[pd.DataFrame, Dict[str, float]]:
        r = ref_df[[self.join_key] + self.metrics].copy()
        p = pred_df[[self.join_key] + self.metrics].copy()
        r = self._to_numeric(r, self.metrics)
        p = self._to_numeric(p, self.metrics)

        df = r.merge(p, on=self.join_key, suffixes=("_ref", "_pred"))
        if df.empty:
            raise ValueError(
                "No overlapping rows between reference and prediction after join."
            )

        rows = []
        for m in self.metrics:
            err = df[f"{m}_pred"] - df[f"{m}_ref"]
            mae = err.abs().mean(skipna=True)
            rmse = math.sqrt((err.pow(2)).mean(skipna=True))
            n = err.notna().sum()
            rows.append({"metric": m, "MAE": mae, "RMSE": rmse, "N": n})
        per_metric = pd.DataFrame(rows)

        overall = {
            "AME_macro": per_metric["MAE"].mean(),
            "RMSE_macro": per_metric["RMSE"].mean(),
            "rows_evaluated": len(df),
        }

        pooled_abs, pooled_sq = [], []
        for m in self.metrics:
            e = (df[f"{m}_pred"] - df[f"{m}_ref"]).dropna()
            pooled_abs.extend(e.abs().tolist())
            pooled_sq.extend((e**2).tolist())
        overall.update(
            {
                "MAE_micro": float(pd.Series(pooled_abs).mean())
                if pooled_abs
                else float("nan"),
                "RMSE_micro": math.sqrt(pd.Series(pooled_sq).mean())
                if pooled_sq
                else float("nan"),
            }
        )

        return per_metric, overall

    @staticmethod
    def load_reference(
        dataset_name="dongx1997/NutriBench", split="train", n=50
    ) -> pd.DataFrame:
        ds = load_dataset(dataset_name)
        return ds[split].select(range(n)).to_pandas()

    @staticmethod
    def load_predictions(csv_path: str) -> pd.DataFrame:
        return pd.read_csv(csv_path)


if __name__ == "__main__":
    hf_ref = NutritionEvaluator.load_reference("dongx1997/NutriBench", "train", 50)
    pred_df = NutritionEvaluator.load_predictions("../data/nutribench_estimated.csv")

    evaluator = NutritionEvaluator()
    per_metric, overall = evaluator.evaluate(hf_ref, pred_df)

    print(per_metric)
    print(overall)

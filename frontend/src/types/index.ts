export interface ModelMetric {
  model_name: string;
  train_mae: number;
  train_rmse: number;
  train_r2: number;
  test_mae: number;
  test_rmse: number;
  test_r2: number;
  cv_mae_mean: number;
  cv_mae_std: number;
  cv_r2_mean: number;
}

export interface PredictionRequest {
  case_seq_no: number;
  filing_year: number;
  filing_month: number;
  filing_day_of_week?: number;
  filing_day_of_year: number;
}

export interface PredictionResponse {
  estimated_duration_days: number;
  model_used: string;
  baseline_comparison_days: number;
  confidence_interval_95: {
    lower_bound_days: number;
    upper_bound_days: number;
  };
  advisory_notice: string;
}

export interface RankingExplanation {
  filingnumber: string;
  filing_date: string;
  observed_age_days: number;
  procedural_score: number;
  rank: number;
  primary_factors: string[];
}

export interface RankingQueueResponse {
  total_records_returned: number;
  queue: RankingExplanation[];
}

export interface EdaSummary {
  total_cases: number;
  disposed_cases: number;
  pending_cases: number;
  disposal_rate: number;
  disposed_duration_mean: number;
  disposed_duration_std: number;
  disposed_duration_median: number;
  disposed_duration_iqr: number;
  disposed_duration_min: number;
  disposed_duration_max: number;
  skewness: number;
  kurtosis: number;
}

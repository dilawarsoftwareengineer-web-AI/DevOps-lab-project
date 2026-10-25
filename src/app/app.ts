import { CommonModule } from '@angular/common';
import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { FEATURE_SCHEMA, FeatureSchemaItem } from './feature-schema';
import { PredictionResponse, PredictionService } from './prediction.service';

interface ModelMetric {
  model: string;
  accuracy: number;
  precision: number;
  recall: number;
  f1: number;
  roc_auc: number;
  pr_auc: number;
}

@Component({
  selector: 'app-root',
  imports: [CommonModule, FormsModule],
  styleUrl: './app.css',
  templateUrl: './app.html',
})
export class App {
  readonly featureSchema = FEATURE_SCHEMA;
  readonly modelMetrics: ModelMetric[] = [
    { model: 'XGBoost', accuracy: 0.9995, precision: 0.8804, recall: 0.8265, f1: 0.8526, roc_auc: 0.9782, pr_auc: 0.8745 },
    { model: 'Random Forest', accuracy: 0.9991, precision: 0.7094, recall: 0.8469, f1: 0.7721, roc_auc: 0.9821, pr_auc: 0.8486 },
    { model: 'Logistic Regression', accuracy: 0.9755, precision: 0.0610, recall: 0.9184, f1: 0.1144, roc_auc: 0.9721, pr_auc: 0.7189 },
  ];

  formData: Record<string, number> = {
    Time: 0,
    V1: 0,
    V2: 0,
    V3: 0,
    V4: 0,
    V5: 0,
    V6: 0,
    V7: 0,
    V8: 0,
    V9: 0,
    V10: 0,
    V11: 0,
    V12: 0,
    V13: 0,
    V14: 0,
    V15: 0,
    V16: 0,
    V17: 0,
    V18: 0,
    V19: 0,
    V20: 0,
    V21: 0,
    V22: 0,
    V23: 0,
    V24: 0,
    V25: 0,
    V26: 0,
    V27: 0,
    V28: 0,
    Amount: 100,
  };

  prediction: PredictionResponse | null = null;
  loading = false;
  errorMessage = '';
  apiStatus = 'Public live prediction requires the Flask backend to be running locally.';

  constructor(private predictionService: PredictionService) {}

  get featureFields(): FeatureSchemaItem[] {
    return this.featureSchema;
  }

  onSubmit(): void {
    const payload = this.buildPayload();
    const invalid = this.featureSchema.find((field) => {
      const value = payload[field.name];
      return value === undefined || value === null || Number.isNaN(value) || value < field.min || value > field.max;
    });

    if (invalid) {
      this.errorMessage = `Please enter a valid value for ${invalid.label} within the allowed range.`;
      this.prediction = null;
      return;
    }

    this.loading = true;
    this.errorMessage = '';
    this.prediction = null;

    this.predictionService.predict(payload).subscribe({
      next: (response) => {
        this.loading = false;
        this.prediction = response;
        this.apiStatus = response?.status === 'ok' ? 'Live prediction responded successfully.' : 'API call returned a non-success response.';
      },
      error: (err) => {
        this.loading = false;
        this.errorMessage = err?.error?.error || 'The prediction API is unavailable. Please start Flask locally and retry.';
        this.apiStatus = 'The local Flask backend is not responding.';
      },
    });
  }

  buildPayload(): Record<string, number> {
    return Object.fromEntries(this.featureSchema.map((field) => [field.name, this.formData[field.name] ?? field.defaultValue]));
  }

  formatMetric(value: number): string {
    return value.toFixed(4);
  }
}

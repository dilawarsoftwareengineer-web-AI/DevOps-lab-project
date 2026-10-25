import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';

export interface PredictionResponse {
  status: string;
  prediction: number;
  label: string;
  probability?: number;
  error?: string;
}

@Injectable({ providedIn: 'root' })
export class PredictionService {
  constructor(private http: HttpClient) {}

  predict(payload: Record<string, number>): Observable<PredictionResponse> {
    return this.http.post<PredictionResponse>('/api/predict', payload);
  }
}

export interface FeatureSchemaItem {
  name: string;
  label: string;
  min: number;
  max: number;
  step: number;
  defaultValue: number;
}

export const FEATURE_SCHEMA: FeatureSchemaItem[] = [
  { name: 'Time', label: 'Time', min: 0, max: 172792, step: 1, defaultValue: 0 },
  { name: 'V1', label: 'V1', min: -30, max: 30, step: 0.0001, defaultValue: 0 },
  { name: 'V2', label: 'V2', min: -30, max: 30, step: 0.0001, defaultValue: 0 },
  { name: 'V3', label: 'V3', min: -30, max: 30, step: 0.0001, defaultValue: 0 },
  { name: 'V4', label: 'V4', min: -30, max: 30, step: 0.0001, defaultValue: 0 },
  { name: 'V5', label: 'V5', min: -30, max: 30, step: 0.0001, defaultValue: 0 },
  { name: 'V6', label: 'V6', min: -30, max: 30, step: 0.0001, defaultValue: 0 },
  { name: 'V7', label: 'V7', min: -30, max: 30, step: 0.0001, defaultValue: 0 },
  { name: 'V8', label: 'V8', min: -30, max: 30, step: 0.0001, defaultValue: 0 },
  { name: 'V9', label: 'V9', min: -30, max: 30, step: 0.0001, defaultValue: 0 },
  { name: 'V10', label: 'V10', min: -30, max: 30, step: 0.0001, defaultValue: 0 },
  { name: 'V11', label: 'V11', min: -30, max: 30, step: 0.0001, defaultValue: 0 },
  { name: 'V12', label: 'V12', min: -30, max: 30, step: 0.0001, defaultValue: 0 },
  { name: 'V13', label: 'V13', min: -30, max: 30, step: 0.0001, defaultValue: 0 },
  { name: 'V14', label: 'V14', min: -30, max: 30, step: 0.0001, defaultValue: 0 },
  { name: 'V15', label: 'V15', min: -30, max: 30, step: 0.0001, defaultValue: 0 },
  { name: 'V16', label: 'V16', min: -30, max: 30, step: 0.0001, defaultValue: 0 },
  { name: 'V17', label: 'V17', min: -30, max: 30, step: 0.0001, defaultValue: 0 },
  { name: 'V18', label: 'V18', min: -30, max: 30, step: 0.0001, defaultValue: 0 },
  { name: 'V19', label: 'V19', min: -30, max: 30, step: 0.0001, defaultValue: 0 },
  { name: 'V20', label: 'V20', min: -30, max: 30, step: 0.0001, defaultValue: 0 },
  { name: 'V21', label: 'V21', min: -30, max: 30, step: 0.0001, defaultValue: 0 },
  { name: 'V22', label: 'V22', min: -30, max: 30, step: 0.0001, defaultValue: 0 },
  { name: 'V23', label: 'V23', min: -30, max: 30, step: 0.0001, defaultValue: 0 },
  { name: 'V24', label: 'V24', min: -30, max: 30, step: 0.0001, defaultValue: 0 },
  { name: 'V25', label: 'V25', min: -30, max: 30, step: 0.0001, defaultValue: 0 },
  { name: 'V26', label: 'V26', min: -30, max: 30, step: 0.0001, defaultValue: 0 },
  { name: 'V27', label: 'V27', min: -30, max: 30, step: 0.0001, defaultValue: 0 },
  { name: 'V28', label: 'V28', min: -30, max: 30, step: 0.0001, defaultValue: 0 },
  { name: 'Amount', label: 'Amount', min: 0, max: 30000, step: 0.01, defaultValue: 100 },
];

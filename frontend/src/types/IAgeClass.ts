export interface IAgeClass {
  id: number;
  age_class_id?: number,
  name: string;
  minimum_age?: number | null;
  maximum_age?: number | null;
  sex: string;
}

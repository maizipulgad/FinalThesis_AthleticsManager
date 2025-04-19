import type {IRound} from "@/types/IRound";

export interface IJumpHeight {
  jump_height_id: number;
  round: IRound;
  height: number;
  order: number;
}

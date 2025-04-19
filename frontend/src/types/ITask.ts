export interface ITask {
  id: string
  taskName: string
  taskSort: number
  createdDt: string
  dueDt: string
  isCompleted: boolean
  isArchived: boolean
  todoCategoryId: string
  todoPriorityId: string
  syncDt: string
}

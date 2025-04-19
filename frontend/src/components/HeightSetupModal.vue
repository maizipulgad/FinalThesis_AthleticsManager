<template>
  <div class="modal-overlay" @click="closeModal">
    <div class="modal" tabindex="-1" style="display: block;">

      <div class="modal-dialog" @click.stop>
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Lisa kõrgused</h5>
            <button type="button" class="btn-close" @click="closeModal"></button>
          </div>
          <div class="modal-body">
            <div class="mb-3">
              <label class="form-label">Algkõrgus (nt 1.20)</label>
              <input v-model.number="startingHeight" type="number" class="form-control" step="0.01" />
            </div>

            <div class="mb-3">
              <label class="form-label">Samm (cm)</label>
              <input v-model.number="step" type="number" class="form-control" />
            </div>

            <div class="mb-3">
              <label class="form-label">Korduste arv</label>
              <input v-model.number="numberOfSteps" type="number" class="form-control" />
            </div>

            <button class="btn btn-secondary mb-3" @click="generateHeights">Lisa kõrgused</button>

            <ul class="list-group mb-3">
              <li v-for="(height, index) in heightList" :key="index" class="list-group-item d-flex justify-content-between">
                {{ height.toFixed(2) }} m
                <button class="btn btn-sm btn-danger" @click="removeHeight(index)">Eemalda</button>
              </li>
            </ul>

            <button class="btn btn-success" @click="saveHeights">Salvesta</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import JumpHeightService from '@/services/JumpHeightService'
import { useRoute } from 'vue-router'

const emit = defineEmits(['close', 'heightsSaved'])
const route = useRoute()

const startingHeight = ref<number | null>(null)
const step = ref<number>(5)
const numberOfSteps = ref<number>(3)
const heightList = ref<number[]>([])

const roundId = Number(route.query.round_id)

const generateHeights = () => {
  const start = parseFloat(String(startingHeight.value))
  if (isNaN(start) || step.value <= 0 || numberOfSteps.value <= 0) return

  const newHeights: number[] = []
  let base = heightList.value.length > 0 ? heightList.value[heightList.value.length - 1] : start

  for (let i = 0; i < numberOfSteps.value; i++) {
    const height = parseFloat((base + i * step.value / 100).toFixed(2))
    if (!heightList.value.includes(height)){
      newHeights.push(height)
    }
  }

  heightList.value.push(...newHeights)
}

const removeHeight = (index: number) => {
  heightList.value.splice(index, 1)
}

const saveHeights = async () => {
  const payload = heightList.value.map((h, index) => ({
    round: roundId,
    height: h,
    order: index + 1,
  }));

  const response = await JumpHeightService.saveHeights(payload)
  if (response.data) {
    emit('heightsSaved')
    emit('close')
  } else {
    alert('Failed to save heights')
  }
}

const closeModal = () => emit('close')
</script>


<style scoped>
.modal {
  background-color: rgba(0, 0, 0, 0.5);
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  display: flex;
  justify-content: center;
  align-items: center;
}

.modal-dialog {
  max-width: 500px;
}
</style>

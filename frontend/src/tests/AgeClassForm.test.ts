import { render, screen, fireEvent } from '@testing-library/vue'
import AgeClassForm from '@/views/ageclasses/AgeClassForm.vue'
import { createRouter, createMemoryHistory } from 'vue-router'
import { describe, it, expect, vi } from 'vitest'
import { flushPromises } from '@vue/test-utils'

// Mock service
vi.mock('@/services/AgeClassService', () => ({
  default: {
    createAgeClass: vi.fn().mockResolvedValue({}),
    updateAgeClass: vi.fn().mockResolvedValue({}),
    getAgeClassById: vi.fn().mockResolvedValue({
      data: {
        id: 1,
        name: 'U14',
        minimum_age: 12,
        maximum_age: 13,
        sex: 'F'
      }
    })
  }
}))

// Router
const router = createRouter({
  history: createMemoryHistory(),
  routes: [
    { path: '/age-classes', name: 'AgeClassList', component: { template: '<div>List</div>' } },
    { path: '/ageclasses/edit/:id', name: 'EditAgeClass', component: AgeClassForm },
    { path: '/ageclasses/add', name: 'AddAgeClass', component: AgeClassForm }
  ]
})

describe('AgeClassForm.vue', () => {
  it('Fill and submit new form to add age class', async () => {
    render(AgeClassForm, {
      global: { plugins: [router] }
    })

    await fireEvent.update(screen.getByLabelText('Nimi:'), 'U16')
    await fireEvent.update(screen.getByLabelText('Min iga (aastates):'), '14')
    await fireEvent.update(screen.getByLabelText('Max iga (aastates):'), '15')
    await fireEvent.update(screen.getByLabelText('Sugu:'), 'M')

    await fireEvent.click(screen.getByRole('button', { name: 'Lisa' }))
  })

  it('display existing age class and send update', async () => {
    await router.push('/ageclasses/edit/1')
    await router.isReady()

    render(AgeClassForm, {
      global: { plugins: [router] }
    })

    await flushPromises()

    expect(await screen.findByDisplayValue('U14')).toBeTruthy()
    expect(screen.getByDisplayValue('12')).toBeTruthy()
    expect(screen.getByDisplayValue('13')).toBeTruthy()

    await fireEvent.update(screen.getByLabelText('Nimi:'), 'U14 Muudetud')
    await fireEvent.click(screen.getByRole('button', { name: 'Muuda' }))
  })
})

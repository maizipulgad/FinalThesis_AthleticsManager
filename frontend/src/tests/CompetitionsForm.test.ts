import { render, screen, fireEvent } from '@testing-library/vue'
import CompetitionsForm from '@/views/competitions/CompetitionsForm.vue'
import { createRouter, createMemoryHistory } from 'vue-router'
import { describe, it, expect, vi } from 'vitest'
import {flushPromises} from "@vue/test-utils";

// Mock service
vi.mock('@/services/CompetitionService', () => ({
  default: {
    createCompetition: vi.fn(),
    updateCompetition: vi.fn(),
    getCompetitionById: vi.fn().mockResolvedValue({
      data: {
        id: 1,
        name: 'Talvine karikas',
        active: true,
        comments: 'Indoor event',
        startDate: '2025-02-01T10:00',
        endDate: '2025-02-02T18:00',
      }
    })
  }
}))

const router = createRouter({
  history: createMemoryHistory(),
  routes: [
    { path: '/competitions/add', name: 'AddCompetition', component: CompetitionsForm },
    { path: '/competitions/edit/:id', name: 'EditCompetition', component: CompetitionsForm },
    { path: '/competitions', name: 'CompetitionList', component: { template: '<div>List</div>' } }
  ]
})

describe('CompetitionsForm.vue', () => {
  it('fill in the form for a new competition', async () => {
    router.push('/competitions/add')
    await router.isReady()

    render(CompetitionsForm, {
      global: { plugins: [router] }
    })

    await fireEvent.update(screen.getByLabelText('Nimetus:'), 'Sügisene jooks')
    await fireEvent.click(screen.getByLabelText('Aktiivne?'))
    await fireEvent.update(screen.getByLabelText('Kommentaarid:'), 'Rajajooks')
    await fireEvent.update(screen.getByLabelText('Algusaeg:'), '2025-09-01T12:00')
    await fireEvent.update(screen.getByLabelText('Lõppaeg:'), '2025-09-02T16:00')
    await fireEvent.click(screen.getByRole('button', { name: 'Lisa' }))
  })

  it('display existing competitions data and send update', async () => {
    router.push('/competitions/edit/1')
    await router.isReady()

    render(CompetitionsForm, {
      global: { plugins: [router] }
    })

    await flushPromises()

    expect(await screen.findByDisplayValue('Talvine karikas')).toBeTruthy()
    expect(screen.getByDisplayValue('Indoor event')).toBeTruthy()

    await fireEvent.update(screen.getByLabelText('Nimetus:'), 'Talvine karikas 2025')
    await fireEvent.click(screen.getByRole('button', { name: 'Muuda' }))
  })
})

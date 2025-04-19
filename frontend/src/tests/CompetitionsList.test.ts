import { render, screen } from '@testing-library/vue'
import CompetitionsList from '@/views/competitions/CompetitionsList.vue'
import { createRouter, createMemoryHistory } from 'vue-router'
import { describe, it, expect, vi } from 'vitest'
import '@testing-library/jest-dom'

// Mock service
vi.mock('@/services/CompetitionService', () => ({
  default: {
    getAllCompetitions: vi.fn().mockResolvedValue({
      data: [
        {
          id: 1,
          name: 'Test võistlus 1',
          active: true,
          comments: 'Kommentaarid 1',
          startDate: '2025-01-16T12:00:00Z',
          endDate: '2025-01-17T22:00:00Z'
        },
        {
          id: 2,
          name: 'Test võistlus 2',
          active: false,
          comments: 'Kommentaarid 2',
          startDate: '2025-01-20T12:00:00Z',
          endDate: '2025-01-21T22:00:00Z'
        }
      ]
    })
  }
}))

const router = createRouter({
  history: createMemoryHistory(),
  routes: [
    { path: '/', name: 'CompetitionsList', component: CompetitionsList },
    { path: '/competitions/edit/:id', name: 'EditCompetition', component: { template: '<div>Edit</div>' } }
  ]
})

describe('CompetitionsList.vue', () => {
  it('display table and button "Lisa võistlus"', async () => {
    render(CompetitionsList, {
      global: { plugins: [router] }
    })

    expect(await screen.findByText('Lisa võistlus')).toBeTruthy()
    expect(await screen.findByText('Test võistlus 1')).toBeTruthy()
    expect(await screen.findByText('Test võistlus 2')).toBeTruthy()
  })

  it('display checkbox only for active competitions', async () => {
    render(CompetitionsList, {
      global: { plugins: [router] }
    })

    const checkboxes = await screen.findAllByRole('checkbox')
    expect(checkboxes).toHaveLength(2)
    expect(checkboxes[0]).toBeChecked()
    expect(checkboxes[1]).not.toBeChecked()
  })
})

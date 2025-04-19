import { describe, it, expect, vi, beforeEach } from 'vitest'
import { render, screen, within } from '@testing-library/vue'
import AgeClassList from '@/views/ageClasses/AgeClassesList.vue'
import { createRouter, createWebHistory } from 'vue-router'

// Mock router
const router = createRouter({
  history: createWebHistory(),
  routes: []
})

// Mock service
vi.mock('@/services/AgeClassService', () => ({
  default: {
    getAllAgeClasses: () => Promise.resolve({
      data: [
        { id: 1, name: 'U14', minimum_age: 12, maximum_age: 13, sex: 'M' },
        { id: 2, name: 'U16', minimum_age: 14, maximum_age: 15, sex: 'F' }
      ],
      errors: null
    })
  }
}))

describe('AgeClassList.vue', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  it('Displays heading and button "Lisa vanuseklass"', async () => {
    render(AgeClassList, {
      global: {
        plugins: [router]
      }
    })

    expect(await screen.findByText('Vanuseklassid')).toBeTruthy()
    expect(screen.getByRole('button', { name: 'Lisa vanuseklass' })).toBeTruthy()
  })

  it('Display table with 2 age class', async () => {
    render(AgeClassList, {
      global: {
        plugins: [router]
      }
    })

      expect(await screen.findByText('U14')).toBeTruthy()
      expect(screen.getByText('U16')).toBeTruthy()

      const rowgroups = screen.getAllByRole('rowgroup')
      const tbody = rowgroups.find(el => el.tagName.toLowerCase() === 'tbody')!
      const muudaLinks = within(tbody).getAllByText('Muuda')
      expect(muudaLinks).toHaveLength(2)
  })
})

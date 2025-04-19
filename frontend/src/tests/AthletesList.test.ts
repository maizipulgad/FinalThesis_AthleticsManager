import { render, screen, fireEvent, within } from '@testing-library/vue'
import AthletesList from '@/views/athletes/AthletesList.vue'
import { describe, it, expect, vi } from 'vitest'
import { createRouter, createMemoryHistory } from 'vue-router'

// Mock data
vi.mock('@/services/AthleteService', () => ({
  default: {
    getAllAthletes: vi.fn().mockResolvedValue({
      data: [
        { id: 1, firstName: 'Jaan', lastName: 'Tamm', dateOfBirth: '2000-01-01', sex: 'M' },
        { id: 2, firstName: 'Mari', lastName: 'Kask', dateOfBirth: '2001-02-02', sex: 'F' },
        { id: 3, firstName: 'Jaanika', lastName: 'Piir', dateOfBirth: '2002-03-03', sex: 'F' },
      ]
    })
  }
}))



// Router
const router = createRouter({
  history: createMemoryHistory(),
  routes: [
    {
      path: '/',
      name: 'AthletesList',
      component: AthletesList
    },
    {
      path: '/athletes/edit/:id',
      name: 'EditAthlete',
      component: { template: '<div>Edit Page</div>' }
    },
    {
      path: '/athletes/add',
      name: 'AddAthlete',
      component: { template: '<div>Add Page</div>' }
    }
  ]
})

describe('AthletesList.vue', () => {
  it('Display table and button "Lisa võistleja"', async () => {
    render(AthletesList, {
      global: {
        plugins: [router]
      }
    })

    expect(await screen.findByText('Lisa võistleja')).toBeTruthy()
    expect(await screen.findByText('Jaan')).toBeTruthy()
    expect(await screen.findByText('Mari')).toBeTruthy()
       expect(await screen.findByText('Jaanika')).toBeTruthy()

  })

  it('Filter athletes by name', async () => {
    render(AthletesList, {
      global: {
        plugins: [router]
      }
    })

    const input = (await screen.findAllByPlaceholderText('Otsi ees- või perenime järgi'))[0]
    await fireEvent.update(input, 'Jaan')

    await new Promise(resolve => setTimeout(resolve, 0))

    const tbody = screen.getAllByRole('rowgroup').find(el => el.tagName.toLowerCase() === 'tbody')!
    const allRows = within(tbody).getAllByRole('row')

    const filteredRows = allRows.filter(row => row.textContent?.includes('Jaan'))
    expect(filteredRows).toHaveLength(2)

    const containsMari = allRows.some(row => row.textContent?.includes('Mari'))
    expect(containsMari).toBe(false)

  })
})

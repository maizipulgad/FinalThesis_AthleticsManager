import { render, screen, fireEvent } from '@testing-library/vue'
import { describe, it, expect, vi, beforeEach } from 'vitest'
import AthleteForm from '@/views/athletes/AthleteForm.vue'
import { createRouter, createMemoryHistory } from 'vue-router'

// Mocked service
vi.mock('@/services/AthleteService', () => ({
  default: {
    getAthleteById: vi.fn().mockResolvedValue({
      data: {
        id: 1,
        firstName: 'Edit',
        lastName: 'User',
        dateOfBirth: '1990-01-01',
        sex: 'M',
      },
    }),
    createAthlete: vi.fn().mockResolvedValue({}),
    updateAthlete: vi.fn().mockResolvedValue({}),
  }
}))

const routes = [
  {
    path: '/athletes',
    name: 'AthletesList',
    component: { template: '<div>Athletes List</div>' }
  },
  {
    path: '/athletes/edit/:id',
    name: 'EditAthlete',
    component: AthleteForm
  },
  {
    path: '/athletes/add',
    name: 'AddAthlete',
    component: AthleteForm
  }
]

const router = createRouter({
  history: createMemoryHistory(),
  routes
})


describe('AthleteForm.vue', () => {
  it('Displays heading "Lisa võistleja"', async () => {
    router.push('/athletes/add')
    await router.isReady()

    render(AthleteForm, {
      global: { plugins: [router] }
    })

    expect(await screen.findByText('Lisa võistleja')).toBeTruthy()
  })

  it('Fill and submit the form of athlete', async () => {
    router.push('/athletes/add')
    await router.isReady()

    render(AthleteForm, {
      global: { plugins: [router] }
    })

    await fireEvent.update(screen.getByLabelText('Eesnimi:'), 'Test')
    await fireEvent.update(screen.getByLabelText('Perenimi:'), 'User')
    await fireEvent.update(screen.getByLabelText('Sünniaeg:'), '1995-05-15')
    await fireEvent.update(screen.getByLabelText('Sugu:'), 'F')

    const buttons = screen.getAllByRole('button', { name: 'Lisa' })
    await fireEvent.click(buttons[0])
  })

})
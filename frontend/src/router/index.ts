import Home from '@/views/Home.vue'
import Login from '@/views/Login.vue'
import Logout from '@/views/Logout.vue'
import AthletesList from '@/views/athletes/AthletesList.vue'
import AthleteForm from '@/views/athletes/AthleteForm.vue'

import { createRouter, createWebHistory } from 'vue-router';
import { useAuthStore } from '@/stores/auth';
import CompetitionsList from "@/views/competitions/CompetitionsList.vue";
import CompetitionsForm from "@/views/competitions/CompetitionsForm.vue";
import CompetitionAthletes from "@/views/CompetitionAthletes/CompetitionAthletes.vue";
import CompetitionEventAthletes from "@/views/competitionEvents/CompetitionEventAthletes.vue";
import ManageCompetitionAthletes from "@/views/CompetitionAthletes/ManageCompetitionAthletes.vue";
import JumpAndThrowResultsPage from "@/views/results/JumpAndThrowResultsPage.vue";
import HighJumpAndPoleVaultPage from "@/views/results/HighJumpAndPoleVaultPage.vue";
import RunningResultsPage from "@/views/results/RunningResultsPage.vue";
import AgeClassesList from "@/views/ageClasses/AgeClassesList.vue";
import AgeClassForm from "@/views/ageClasses/AgeClassForm.vue";
import CollectivesList from "@/views/collectives/CollectivesList.vue";
import CollectiveForm from "@/views/collectives/CollectiveForm.vue";




const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    { path: '/', name: 'Home', component: Home },
    { path: '/home', name: 'Home', component: Home },
    { path: '/login', name: 'Login', component: Login },
    { path: '/logout', name: 'Logout', component: Logout    },

      // ATHLETES
    { path: '/athletes', name: 'AthletesList', component: AthletesList },
    { path: '/athletes/add', name: 'AthleteFormAdd', component: AthleteForm },
    { path: '/athletes/edit/:id', name: 'AthleteFormEdit', component: AthleteForm },

      //COMPETITON
    { path: '/competitions', name: 'CompetitionsList', component: CompetitionsList },
    { path: '/competitions/add', name: 'CompetitionFormAdd', component: CompetitionsForm },
    { path: '/competitions/edit/:id', name: 'CompetitionFormEdit', component: CompetitionsForm },

      //AGECLASSES
    { path: '/age-classes', name: 'AgeClassesList', component: AgeClassesList },
     { path: '/ageclasses/add', name: 'AgeClassFormAdd', component: AgeClassForm },
     { path: '/ageclasses/edit/:id', name: 'AgeClassFormEdit', component: AgeClassForm },

      //COLLECTIVES
    { path: '/collectives', name: 'CollectivesList', component: CollectivesList },
     { path: '/collectives/add', name: 'CollectiveFormAdd', component: CollectiveForm },
     { path: '/collectives/edit/:id', name: 'CollectiveFormEdit', component: CollectiveForm },

      //COMPETITION-ATHLETESS
    { path: "/competition-athletes", name: 'CompetitionAthletes', component: CompetitionAthletes },

      //COMPETITON-EVENTS
    { path: "/competition-event/:competition_event_id", name: "CompetitionEventAthletes", component: CompetitionEventAthletes },

      //MANAGE COMPETITION-EVENTS AND ATHLETES (ROUNDS)
    { path: "/competition-event/:competition_event_id/manage-athletes", name: "ManageCompetitionAthletes", component: ManageCompetitionAthletes , props: true},

      // JUMP RESULTS
    { path: "/jump-and-throw-results/:competition_event_id", name: "JumpAndThrowResults", component: JumpAndThrowResultsPage},

      // HIGH-JUMP AND POLE-VAULT RESULTS
    { path: "/high-jump-results/:competition_event_id", name: "HighJumpAndPoleVaultResults", component: HighJumpAndPoleVaultPage},

    // RUNNING RESULTS
    { path: "/running-results/:competition_event_id", name: "RunningResults", component: RunningResultsPage},

  ]
})


// Add a global navigation guard
router.beforeEach((to, from, next) => {
  const authStore = useAuthStore();

  // Check if the route requires authentication
  if (to.name !== 'Login' && !authStore.isAuthenticated) {
    // Redirect to the login page if the user is not authenticated
    next({ name: 'Login' });
  } else {
    // Proceed to the requested route
    next();
  }
});

export default router

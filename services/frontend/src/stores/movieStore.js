import { defineStore } from 'pinia'

export const useMovieStore = defineStore({
  id: 'movie',
  state: () => ({
    selectedMovie: null
  }),
  getters: {
    getSelectedMovie() {
      return this.selectedMovie
    }
  },
  actions: {
    setSelectedMovie(movie) {
      this.selectedMovie = movie
      localStorage.setItem('selectedMovie', JSON.stringify(movie))
      console.log('selectedMovie', this.selectedMovie)
    }
  }
})

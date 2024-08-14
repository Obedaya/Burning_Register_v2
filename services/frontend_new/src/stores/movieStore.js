// src/stores/movieStore.js
import { defineStore } from 'pinia';

export const useMovieStore = defineStore({
  id: 'movie',
  
  state: () => ({
    selectedMovie: localStorage.getItem('selectedMovie') 
                   ? JSON.parse(localStorage.getItem('selectedMovie')) 
                   : null,
  }),

  
  actions: {
    selectMovie(movie) {
      this.selectedMovie = movie;
      localStorage.setItem('selectedMovie', JSON.stringify(movie));
    },
    
    clearMovieSelection() {
      this.selectedMovie = null;
      localStorage.removeItem('selectedMovie');
    }
  }
});

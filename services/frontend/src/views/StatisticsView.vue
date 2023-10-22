<template>
  <v-container fluid>
    <!-- Movie Selection Dropdown -->
    <v-row>
      <v-col>
        <!-- Movie Selection Dropdown -->
        <v-select
          v-model="selectedMovie"
          :items="movies"
          item-title="name"
          item-value="_id"
          label="Select a movie"
          return-object
        ></v-select>
      </v-col>
    </v-row>
    <!-- Display Information about the selected movie here -->
    <v-row>
      <v-col cols="4">
        <v-card>
          <v-card-title>Movie Details</v-card-title>
          <v-card-text>
            <div v-if="selectedMovie">
              <p><strong>Title:</strong> {{ selectedMovie.name }}</p>
              <p><strong>Room:</strong> {{ selectedMovie.room }}</p>
              <p><strong>Date:</strong> {{ selectedMovie.datetime }}</p>
              <!-- Add more movie details here -->
            </div>
          </v-card-text>
        </v-card>
      </v-col>
      <v-col cols="8">
        <v-card class="overflow-y-auto" max-height="400">
          <v-card-title>Statistics</v-card-title>
          <v-card-text>
            <h4>Total Sold:</h4>
            {{ total_sold }}€
            <h4>Total Sold to the Team:</h4>
            {{ total_sold_team }}€
            <h4>Total Sold without Pfand:</h4>
            {{ total_sold_without_pfand }}€
            <h4>Tickets Sold:</h4>
            {{ tickets_sold }}x
            <h4>Tickets Sold to the Team:</h4>
            {{ tickets_sold_team }}x
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>
  
<script>
import axios from "axios";
import { useMovieStore } from "@/stores/movieStore";
import { ref, watch } from "vue";

export default {
  data() {
    return {
      movies: [
        {
          _id: "1",
          name: "Chihiros Reise ins Zauberland",
          datetime: "2023-06-14T19:30:00.000+00:00",
          room: "J007",
        },
      ],
      total_sold: 0,
      total_sold_team: 0,
      total_sold_without_pfand: 0,
      tickets_sold: 0,
      tickets_sold_team: 0,
    };
  },
  setup() {
    const movieStore = useMovieStore();

    // Initialize selectedMovie with the value from the store
    const selectedMovie = ref(movieStore.selectedMovie);

    watch(selectedMovie, (newVal) => {
      movieStore.selectMovie(newVal);
      console.log(movieStore.selectedMovie);
    });

    return {
      selectedMovie,
    };
  },
  methods: {
    async getMovies() {
      try {
        const response = await axios.get("/api/v1/movies/", {
          withCredentials: false, // Ensure credentials are not sent
        });
        this.movies = response.data;
      } catch (error) {
        console.error(error);
      }
    },
    async getTotal() {
      try {
        const response = await this.getTotalInfo(
          this.selectedMovie.name,
          false,
          false,
          false
        );
        this.total_sold = response;
      } catch (error) {
        console.error(error);
      }
    },
    async getTotalTeam() {
      try {
        const response = await this.getTotalInfo(
          this.selectedMovie.name,
          true,
          false,
          false
        );
        this.total_sold_team = response;
      } catch (error) {
        console.error(error);
      }
    },
    async getTotalWithoutPfand() {
      try {
        const response = await this.getTotalInfo(
          this.selectedMovie.name,
          false,
          false,
          true
        );
        this.total_sold_without_pfand = response;
      } catch (error) {
        console.error(error);
      }
    },
    async getTickets() {
      try {
        const response = await this.getTicketInfo(
          this.selectedMovie.name,
          false,
          false,
          true
        );
        this.tickets_sold = response;
      } catch (error) {
        console.error(error);
      }
    },
    async getTicketsTeam() {
      try {
        const response = await this.getTicketInfo(
          this.selectedMovie.name,
          true,
          false,
          true
        );
        this.tickets_sold_team = response;
      } catch (error) {
        console.error(error);
      }
    },
    async getTotalInfo(movie, isteam, cancellation, pfand) {
      try {
        const response = await axios.get(
          `/api/v1/history/total?movie=${movie}&isteam=${isteam}&cancellation=${cancellation}&pfand=${pfand}`,
          {
            withCredentials: false, // Ensure credentials are not sent
          }
        );
        return response.data;
      } catch (error) {
        console.error(error);
      }
    },
    async getTicketInfo(movie, isteam, freeticket) {
      try {
        const response = await axios.get(
          `/api/v1/history/tickets?movie=${movie}&isteam=${isteam}&freeticket=${freeticket}`,
          {
            withCredentials: false, // Ensure credentials are not sent
          }
        );
        return response.data;
      } catch (error) {
        console.error(error);
      }
    },
    async setSelectedMovie() {
      await this.getTotal();
      await this.getTotalTeam();
      await this.getTotalWithoutPfand();
      await this.getTickets();
      await this.getTicketsTeam();
    },
  },
  created() {
    this.getMovies();
  },
  watch: {
    selectedMovie(newMovie, oldMovie) {
      if (newMovie !== oldMovie) {
        this.setSelectedMovie();
      }
    },
  },
};
</script>

  
  <style scoped>
</style>
  
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
          @change="this.setSelectedMovie(selectedMovie)"
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
            <p>{{ calculateTotalAmount() }}</p>
            <h4>Total Sold to the Team:</h4>
            <p>{{ calulateTotalAmountTeam() }}</p>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>
  
  <script>
import axios from "axios";

export default {
  data() {
    return {
      selectedMovie: null,
      movies: [
        {
          _id: "1",
          name: "Chihiros Reise ins Zauberland",
          datetime: "2023-06-14T19:30:00.000+00:00",
          room: "J007",
        },
      ],
      history: [
        {
          _id: "1",
          timestamp: "2023-06-14T19:30:00.000+00:00",
          total: 100,
          isTeam: false,
          movie: "Movie",
          cancellation: false,
          products: [],
        },
        {
          _id: "2",
          timestamp: "2023-06-14T19:30:00.000+00:00",
          total: 50,
          isTeam: false,
          movie: "Movie",
          cancellation: false,
          products: [],
        },
      ],
    };
  },
  methods: {
    getMovies() {
      // Implement logic to fetch movies from the backend
      axios
        .get("/api/v1/movies/", {
          withCredentials: false, // Ensure credentials are not sent
        })
        .then((response) => {
          // Handle success
          this.movies = response.data;
        })
        .catch((error) => {
          // Handle errors
          console.log(error);
        });
    },
    getHistory() {
      console.log(this.selectedMovie);
      axios
        .get("/api/v1/history/?movie=" + this.selectedMovie.name, {
          withCredentials: false, // Ensure credentials are not sent
        })
        .then((response) => {
          // Handle success
          this.history = response.data;
        })
        .catch((error) => {
          // Handle errors
          console.log(error);
        });
    },
    setSelectedMovie() {
      this.getHistory();
    },
    calculateTotalAmount() {
      return this.history.reduce((total, entry) => {
        if (!entry.isTeam && !entry.cancellation) {
          total += entry.total;
        }
        return total;
      }, 0);
    },
    calulateTotalAmountTeam(){
      return this.history.reduce((total, entry) => {
        if (entry.isTeam && !entry.cancellation) {
          total += entry.total;
        }
        return total;
      }, 0);
    },
  },
  created() {
    this.getMovies();
  },
  watch: {
    selectedMovie(newMovie, oldMovie) {
      // This function will be called whenever selectedMovie changes
      if (newMovie !== oldMovie) {
        // Call your API function here
        this.getHistory();
      }
    },
  },
};
</script>
  
  <style scoped>
</style>
  
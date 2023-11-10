<template>
  <v-container fluid>
    <v-dialog v-model="formvisible" max-width="500px">
    <v-card>
      <v-card-title>
        Movie Reservation Form
      </v-card-title>
      <v-card-text>
        <v-form>
          <v-text-field label="Movie Name" v-model="addMovieName"></v-text-field>
          <v-text-field label="Room" v-model="addMovieRoom"></v-text-field>
        </v-form>
      </v-card-text>
      <v-card-actions>
        <v-btn color="primary" @click="saveReservation">Save</v-btn>
        <v-btn color="error" @click="closeDialog">Cancel</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
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

    <!-- Movie Details Card and Orders List -->
    <v-row>
      <v-col cols="4">
        <v-card>
          <v-card-title>Movie Details</v-card-title>
          <v-card-text>
            <div v-if="selectedMovie">
              <p><strong>Title:</strong> {{ selectedMovie.name }}</p>
              <p><strong>Room:</strong> {{ selectedMovie.room }}</p>
              <p><strong>Date:</strong> {{ selectedMovie.datetime }}</p>
            </div>
          </v-card-text>
        </v-card>
        <v-btn @click="formvisible = true" color="primary">Add Movie</v-btn>
      </v-col>

      <v-col cols="8">
        <v-card class="overflow-y-auto" max-height="400">
          <v-card-title>Orders</v-card-title>
          <v-card-text>
            <v-list>
              <v-list-item
                v-for="(order, index) in orders"
                :key="index"
                @click="selectOrder(order)"
                :class="{ 'order-selected': selectedOrder === order }"
              >
                <v-list-item-content>
                  <v-list-item-title>{{
                    order.timestamp
                  }}</v-list-item-title>
                  <v-list-item-subtitle>
                    Total: {{ order.total }}
                    IsTeam: {{ order.isteam }}
                    Products: {{ printProducts(order) }}
                    Canceled: {{ order.cancellation }}
                  </v-list-item-subtitle>
                </v-list-item-content>
              </v-list-item>
            </v-list>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- Cancel Order Button -->
    <v-row>
      <v-col>
        <v-btn v-if="selectedOrder" color="error" @click="cancelSelectedOrder">
          Cancel Selected Order
        </v-btn>
      </v-col>
    </v-row>
  </v-container>
</template>
  
  <script>
import axios from "axios";
import { useMovieStore } from "@/stores/movieStore";
import { ref, watch } from "vue";


export default {
  components: {

  },
  data() {
    return {
      movies: [],
      orders: [],
      selectedOrder: null,
      formvisible: false,
      addMovieName: "",
      addMovieRoom: "",
      addMovieDate: new Date(),
      addMovieTime: new Date(),
    };
  },
  setup() {
    const movieStore = useMovieStore();

    // Initialize selectedMovie with the value from the store
    const selectedMovie = ref(movieStore.selectedMovie);

    watch(selectedMovie, (newVal) => {
      movieStore.selectMovie(newVal);
    });

    return {
      selectedMovie,
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
      // Implement logic to fetch order history from the backend
      axios
        .get("/api/v1/history/?movie=" + this.selectedMovie.name, {
          withCredentials: false, // Ensure credentials are not sent
        })
        .then((response) => {
          // Handle success
          this.orders = response.data;
        })
        .catch((error) => {
          // Handle errors
          console.log(error);
        });
    },
    selectOrder(order) {
      if (this.selectedOrder === order) {
        this.selectedOrder = null;
      } else {
        this.selectedOrder = order;
      }
    },
    cancelSelectedOrder() {
      axios
      .post("/api/v1/history/cancel/?_id=" + this.selectedOrder._id.toString(), {
        withCredentials: false,
      })
      .then(() => {
        this.getHistory();
      })
      .catch((error) => {
        // Handle errors
        console.log(error);
      })
    },
    closeDialog() {
      this.formvisible = false;
    },
    saveReservation() {
      // Implement logic to save the reservation
      this.formvisible = false;
    },
    printProducts(order) {
      let products = "";
      for (let i = 0; i < order.products.length; i++) {
        products += order.products[i].name + " x" + order.products[i].amount;
        if (i < order.products.length - 1) {
          products += ", ";
        }
      }
      return products;
    },
  },
  created() {
    this.getMovies();
    this.getHistory();
  },
  watch: {
    selectedMovie() {
      this.getHistory();
    },
  },
};
</script>
  
  <style scoped>
.order-selected {
  background-color: #ef605a; /* Apply a background color to selected orders */
}
</style>
  
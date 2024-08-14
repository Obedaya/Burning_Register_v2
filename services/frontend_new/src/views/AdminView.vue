<template>
  <v-container fluid>
    <v-dialog v-model="formvisible">
      <v-sheet class="mx-auto w-50">
        <v-form fast-fail @submit.prevent>
          <v-text-field label="Movie Name" v-model="tempMovieName"></v-text-field>
          <v-text-field label="Room" v-model="tempMovieRoom"></v-text-field>
          <v-text-field label="Date and Time" v-model="tempMovieDatetime" :rules="movieDatetimeRule"
            :disabled="datetimeDisabled"></v-text-field>
          <v-text-field label="Trailer" v-model="tempMovieTrailer"></v-text-field>
          <v-text-field label="Description" v-model="tempMovieDescription"></v-text-field>
          <v-text-field label="Language" v-model="tempMovieLanguage"></v-text-field>
          <v-text-field label="Poster" v-model="tempMoviePoster"></v-text-field>
          <v-text-field label="Stripe Payment" v-model="tempMovieStripePayment"></v-text-field>

          <v-btn type="submit" color="primary" @click="submitMovie">Submit</v-btn>
          <v-btn color="error" @click="clearForm">Cancel</v-btn>
        </v-form>
      </v-sheet>
    </v-dialog>
    <!-- Movie Selection Dropdown -->
    <v-row>
      <v-col>
        <!-- Movie Selection Dropdown -->
        <v-select v-model="selectedMovie" :items="movies" item-title="name" item-value="_id" label="Select a movie"
          return-object></v-select>
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
        <v-btn @click="editMovie" color="secondary" v-if="selectedMovie">Edit Movie</v-btn>
        <v-btn @click="downloadReport" color="success">Download Report</v-btn>
      </v-col>

      <v-col cols="8">
        <v-card class="overflow-y-auto" max-height="350">
          <v-card-title>Orders</v-card-title>
          <v-card-text>
            <v-list>
              <v-list-item v-for="(order, index) in orders" :key="index" @click="selectOrder(order)"
                :class="{ 'order-selected': selectedOrder === order }">
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
        <v-card class="overflow-y-auto" max-height="200">
          <v-card-title>Cancelled Orders</v-card-title>
          <v-card-text>
            <v-list>
              <v-list-item v-for="(order, index) in cancelled_orders" :key="index">
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
      cancelled_orders: [],
      selectedOrder: null,
      formvisible: false,
      tempMovieName: "",
      tempMovieRoom: "",
      tempMovieDatetime: new Date().toISOString().slice(0, 19).replace('T', ' '),
      movieDatetimeRule: [
        value => {
          if (/^(19|20)\d\d-(0[1-9]|1[012])-(0[1-9]|[12][0-9]|3[01]) ([01][0-9]|2[0-3]):([0-5][0-9]):([0-5][0-9])$/.test(value)) return true

          return 'Invalid date-time format. Please use the following format: YYYY-MM-DD HH:MM:SS'
        },
      ],
      tempMovieTrailer: "",
      tempMovieDescription: "",
      tempMovieLanguage: "",
      tempMoviePoster: "",
      tempMovieStripePayment: "",
      movieEditing: false,
      datetimeDisabled: false,
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
    downloadReport() {
    axios
      .get('/api/v1/report/report?movie=' + this.selectedMovie.name, { // Make sure to use the correct endpoint
        responseType: 'blob', // Important for files
        withCredentials: false
      })
      .then((response) => {
        // Create a URL for the blob
        const url = window.URL.createObjectURL(new Blob([response.data]));
        // Create an anchor element and click it to download
        const link = document.createElement('a');
        link.href = url;
        link.setAttribute('download', this.selectedMovie.name + '.xlsx'); // or the filename from the response headers
        document.body.appendChild(link);
        link.click();
        // Clean up and remove the link
        link.parentNode.removeChild(link);
      })
      .catch((error) => {
        console.error("There was an error downloading the report:", error);
      });
  },
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
        .get("/api/v1/history/?movie=" + this.selectedMovie.name + "&cancellation=false", {
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
    getHistoryCancelled() {
      // Implement logic to fetch order history from the backend
      axios
        .get("/api/v1/history/?movie=" + this.selectedMovie.name + "&cancellation=true", {
          withCredentials: false, // Ensure credentials are not sent
        })
        .then((response) => {
          // Handle success
          this.cancelled_orders = response.data;
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
    submitMovie() {
      if (this.movieEditing) {
        this.editMovieToDB();
      } else {
        this.addMovieToDB();
      }
      this.clearForm();
    },
    clearForm() {
      this.tempMovieName = "";
      this.tempMovieRoom = "";
      this.tempMovieDatetime = new Date().toISOString().slice(0, 19).replace('T', ' ');
      this.tempMovieTrailer = "";
      this.tempMovieDescription = "";
      this.tempMovieLanguage = "";
      this.tempMoviePoster = "";
      this.tempMovieStripePayment = "";

      this.movieEditing = false;
      this.datetimeDisabled = false;
      this.formvisible = false;
    },
    addMovieToDB() {
      const movie = {
        name: this.tempMovieName,
        datetime: new Date(this.tempMovieDatetime.replace(/-/g, '/')),
        room: this.tempMovieRoom,
        trailer: this.tempMovieTrailer,
        description: this.tempMovieDescription,
        language: this.tempMovieLanguage,
        poster: this.tempMoviePoster,
        stripe_payment: this.tempMovieStripePayment,
      };
      axios
        .post("/api/v1/movies/", movie, {
          withCredentials: false,
        })
        .then((response) => {
          console.log(response.data);
        })
        .catch((error) => {
          console.log(error);
        });
    },
    editMovie() {
      this.movieEditing = true;
      this.datetimeDisabled = true;
      let datetime = new Date(this.selectedMovie.datetime);
      let formattedDatetime = datetime.toISOString().slice(0, 19).replace('T', ' ');

      // Set default value of input fields to current movie
      this.tempMovieName = this.selectedMovie.name;
      this.tempMovieRoom = this.selectedMovie.room;
      this.tempMovieDatetime = formattedDatetime;
      this.tempMovieTrailer = this.selectedMovie.trailer;
      this.tempMovieDescription = this.selectedMovie.description;
      this.tempMovieLanguage = this.selectedMovie.language;
      this.tempMoviePoster = this.selectedMovie.poster;
      this.tempMovieStripePayment = this.selectedMovie.stripe_payment;

      this.formvisible = true;
    },
    editMovieToDB() {
      const movie = {
        name: this.tempMovieName,
        room: this.tempMovieRoom,
        trailer: this.tempMovieTrailer,
        description: this.tempMovieDescription,
        language: this.tempMovieLanguage,
        poster: this.tempMoviePoster,
        stripe_payment: this.tempMovieStripePayment,
      };
      axios
        .put("/api/v1/movies/" + this.selectedMovie._id.toString(), movie, {
          withCredentials: false,
        })
        .then((response) => {
          console.log(response.data);
        })
        .catch((error) => {
          console.log(error);
        });

      this.movieEditing = false;
      this.datetimeDisabled = false;
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
    this.getHistoryCancelled();
  },
  watch: {
    selectedMovie() {
      this.getHistory();
      this.getHistoryCancelled();
    },
  },
};
</script>
  
<style scoped>
.order-selected {
  background-color: #ef605a;
  /* Apply a background color to selected orders */
}
</style>
  
<template>
  <v-container fluid>
    <!-- Movie Selection Dropdown -->
    <v-row>
      <v-col>
        <!-- Movie Selection Dropdown -->
        <v-select v-model="selectedMovie" :items="movies" item-title="name" item-value="_id" label="Select a movie"
          return-object></v-select>
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
        <v-card class="overflow-y-auto">
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
            <h4>Total Tickets with Freitickets:</h4>
            {{ tickets_total }}x
          </v-card-text>
        </v-card>
        <v-card class="overflow-y-auto">
          <v-card-title>Products</v-card-title>
          <v-card-text>
            <v-table>
              <thead>
                <tr>
                  <th class="text-left">Name</th>
                  <th class="text-left">Amount</th>
                  <th class="text-left">Price</th>
                  <th class="text-left">Total</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="product in history_products" :key="product.name">
                  <td>{{ product.name }}</td>
                  <td>{{ product.amount }}</td>
                  <td>{{ product.price }}€</td>
                  <td>{{ product.price * product.amount }}€</td>
                </tr>
              </tbody>
            </v-table>
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
      orders: [
        {
          _id: "2",
          movie: "Chiros Reise ins Zauberland",
          total: "20",
          isTeam: "false",
          products: [
            {
              name: "Cola",
              price: "2",
              amount: "10",
              category: "drinks",
            },
          ],
        }
      ],
      cancelled_orders: [],
      history_products: [],
      total_sold: 0,
      total_sold_team: 0,
      total_sold_without_pfand: 0,
      tickets_sold: 0,
      tickets_total: 0,
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
    async getHistory() {
      try {
        const response = await axios.get(
          "/api/v1/history/?movie=" + this.selectedMovie.name,
          {
            withCredentials: false,
          }
        );
        // Handle success
        const cancelled_orders = [];
        const orders = [];

        response.data.forEach((order) => {
          if (order.cancellation === "true") {
            cancelled_orders.push(order);
          } else {
            orders.push(order);
          }
        });

        this.cancelled_orders = cancelled_orders;
        this.orders = orders;
      } catch (error) {
        // Handle errors
        console.log(error);
      }
    },

    getHistoryProducts() {
      const history_products = [];
      this.orders.forEach((order) => {
        order.products.forEach((product) => {
          if (history_products.find((p) => p.name === product.name)) {
            const index = history_products.findIndex(
              (p) => p.name === product.name
            );
            history_products[index].amount += product.amount;
          } else {
            history_products.push(product);
          } 
        });
      });
      this.history_products = history_products;
    },

    async getTotal() {
      try {
        const response = await this.getTotalInfo(
          this.selectedMovie.name,
          false,
          false,
          true
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
          false
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
          true
        );
        this.tickets_sold = response;
      } catch (error) {
        console.error(error);
      }
    },
    async getTicketsTotal() {
      try {
        const response = await this.getTicketInfo(
          this.selectedMovie.name,
          false,
          false
        );
        this.tickets_total = response;
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
      await this.getHistory();
      this.getHistoryProducts();
      await this.getTotal();
      await this.getTotalTeam();
      await this.getTotalWithoutPfand();
      await this.getTickets();
      await this.getTicketsTotal();
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

  
<style scoped></style>
  
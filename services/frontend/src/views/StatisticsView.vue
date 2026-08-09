<template>
  <v-container fluid class="pa-4 pa-md-6">
    <v-row dense class="mb-4">
      <v-col>
        <v-select
          v-model="selectedMovie"
          :items="movies"
          item-title="name"
          item-value="_id"
          label="Select a movie"
          return-object
          prepend-inner-icon="mdi-movie-open"
          hide-details
        />
      </v-col>
    </v-row>

    <template v-if="selectedMovie">
      <v-row dense class="mb-4">
        <v-col cols="12" md="4">
          <v-card color="surface" class="pa-5 h-100" style="border: 1px solid rgba(255,255,255,0.06);">
            <div class="d-flex align-center mb-3">
              <v-avatar color="primary" variant="tonal" size="40" class="mr-3">
                <v-icon>mdi-movie</v-icon>
              </v-avatar>
              <div class="text-h6 font-weight-bold">Movie Details</div>
            </div>
            <v-divider class="mb-3" />
            <div class="info-row">
              <span class="text-caption text-medium-emphasis">Title</span>
              <span class="text-body-2 font-weight-medium">{{ selectedMovie.name }}</span>
            </div>
            <div class="info-row">
              <span class="text-caption text-medium-emphasis">Room</span>
              <v-chip size="x-small" color="secondary" variant="tonal">{{ selectedMovie.room }}</v-chip>
            </div>
            <div class="info-row">
              <span class="text-caption text-medium-emphasis">Date</span>
              <span class="text-body-2">{{ formatDate(selectedMovie.datetime) }}</span>
            </div>
          </v-card>
        </v-col>

        <v-col cols="12" md="8">
          <v-row dense>
            <v-col cols="6" sm="4">
              <v-card color="surface" class="pa-4 text-center stat-card" style="border: 1px solid rgba(255,255,255,0.06);">
                <v-icon color="primary" size="28" class="mb-2">mdi-cash-multiple</v-icon>
                <div class="text-h5 font-weight-bold text-primary">{{ formatPrice(total_sold) }}</div>
                <div class="text-caption text-medium-emphasis">Total Sold</div>
              </v-card>
            </v-col>
            <v-col cols="6" sm="4">
              <v-card color="surface" class="pa-4 text-center stat-card" style="border: 1px solid rgba(255,255,255,0.06);">
                <v-icon color="success" size="28" class="mb-2">mdi-account-group</v-icon>
                <div class="text-h5 font-weight-bold text-success">{{ formatPrice(total_sold_team) }}</div>
                <div class="text-caption text-medium-emphasis">Team Sales</div>
              </v-card>
            </v-col>
            <v-col cols="6" sm="4">
              <v-card color="surface" class="pa-4 text-center stat-card" style="border: 1px solid rgba(255,255,255,0.06);">
                <v-icon color="secondary" size="28" class="mb-2">mdi-tag-minus</v-icon>
                <div class="text-h5 font-weight-bold text-secondary">{{ formatPrice(total_sold_without_pfand) }}</div>
                <div class="text-caption text-medium-emphasis">Without Pfand</div>
              </v-card>
            </v-col>
            <v-col cols="6" sm="4">
              <v-card color="surface" class="pa-4 text-center stat-card" style="border: 1px solid rgba(255,255,255,0.06);">
                <v-icon color="info" size="28" class="mb-2">mdi-ticket</v-icon>
                <div class="text-h5 font-weight-bold text-info">{{ tickets_sold }}</div>
                <div class="text-caption text-medium-emphasis">Tickets Sold</div>
              </v-card>
            </v-col>
            <v-col cols="6" sm="4">
              <v-card color="surface" class="pa-4 text-center stat-card" style="border: 1px solid rgba(255,255,255,0.06);">
                <v-icon color="warning" size="28" class="mb-2">mdi-ticket-percent</v-icon>
                <div class="text-h5 font-weight-bold text-warning">{{ tickets_total }}</div>
                <div class="text-caption text-medium-emphasis">Total w/ Freitickets</div>
              </v-card>
            </v-col>
            <v-col cols="6" sm="4">
              <v-card color="surface" class="pa-4 text-center stat-card" style="border: 1px solid rgba(255,255,255,0.06);">
                <v-icon color="error" size="28" class="mb-2">mdi-receipt-text</v-icon>
                <div class="text-h5 font-weight-bold">{{ orders.length }}</div>
                <div class="text-caption text-medium-emphasis">Total Orders</div>
              </v-card>
            </v-col>
          </v-row>
        </v-col>
      </v-row>

      <v-row dense>
        <v-col cols="12">
          <v-card color="surface" style="border: 1px solid rgba(255,255,255,0.06);">
            <v-card-title class="d-flex align-center pa-4">
              <v-icon class="mr-2" size="20">mdi-package-variant</v-icon>
              <span class="text-h6 font-weight-bold">Products Sold</span>
            </v-card-title>
            <v-divider />
            <v-table density="comfortable" hover>
              <thead>
                <tr>
                  <th class="text-left font-weight-bold">Product</th>
                  <th class="text-center font-weight-bold">Category</th>
                  <th class="text-center font-weight-bold">Quantity</th>
                  <th class="text-right font-weight-bold">Unit Price</th>
                  <th class="text-right font-weight-bold">Total</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="product in history_products" :key="product.name">
                  <td class="font-weight-medium">{{ product.name }}</td>
                  <td class="text-center">
                    <v-chip size="x-small" variant="tonal" :color="getCategoryColor(product.category)">
                      {{ product.category }}
                    </v-chip>
                  </td>
                  <td class="text-center">{{ product.amount }}x</td>
                  <td class="text-right">{{ formatPrice(product.price) }}</td>
                  <td class="text-right font-weight-bold">{{ formatPrice(product.price * product.amount) }}</td>
                </tr>
              </tbody>
              <tfoot v-if="history_products.length > 0">
                <tr>
                  <td colspan="4" class="text-right font-weight-bold text-body-1">Grand Total</td>
                  <td class="text-right font-weight-bold text-body-1 text-primary">
                    {{ formatPrice(history_products.reduce((sum, p) => sum + p.price * p.amount, 0)) }}
                  </td>
                </tr>
              </tfoot>
            </v-table>
          </v-card>
        </v-col>
      </v-row>
    </template>

    <v-row v-else>
      <v-col cols="12">
        <v-card color="surface" class="pa-12 text-center" style="border: 1px solid rgba(255,255,255,0.06);">
          <v-icon size="64" color="surface-variant" class="mb-4">mdi-chart-bar</v-icon>
          <div class="text-h6 text-medium-emphasis">Select a movie to view statistics</div>
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
      movies: [],
      orders: [],
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
    const selectedMovie = ref(movieStore.selectedMovie);

    watch(selectedMovie, (newVal) => {
      movieStore.selectMovie(newVal);
    });

    return { selectedMovie };
  },
  methods: {
    formatPrice(price) {
      price = parseFloat(price);
      if (Number.isNaN(price)) return "0.00€";
      return `${price.toFixed(2)}€`;
    },
    formatDate(datetime) {
      if (!datetime) return '';
      const d = new Date(datetime);
      return d.toLocaleDateString('de-DE', { day: '2-digit', month: '2-digit', year: 'numeric', hour: '2-digit', minute: '2-digit' });
    },
    getCategoryColor(category) {
      const colors = {
        'Drinks': 'info',
        'Snacks': 'warning',
        'Sweets': 'error',
        'Tickets': 'success',
        'Pfand': 'secondary',
      };
      return colors[category] || 'primary';
    },
    async getMovies() {
      try {
        const response = await axios.get("/api/v1/movies/", { withCredentials: false });
        this.movies = response.data;
      } catch (error) {
        console.error(error);
      }
    },
    async getHistory() {
      try {
        const response = await axios.get(
          "/api/v1/history/?movie=" + this.selectedMovie.name,
          { withCredentials: false }
        );
        const cancelled_orders = [];
        const orders = [];
        response.data.forEach((order) => {
          if (order.cancellation === "true" || order.cancellation === true) {
            cancelled_orders.push(order);
          } else {
            orders.push(order);
          }
        });
        this.cancelled_orders = cancelled_orders;
        this.orders = orders;
      } catch (error) {
        console.log(error);
      }
    },
    getHistoryProducts() {
      const history_products = [];
      this.orders.forEach((order) => {
        order.products.forEach((product) => {
          const existing = history_products.find((p) => p.name === product.name);
          if (existing) {
            existing.amount += product.amount;
          } else {
            history_products.push({ ...product });
          }
        });
      });
      this.history_products = history_products;
    },
    async getTotal() {
      try {
        this.total_sold = await this.getTotalInfo(this.selectedMovie.name, false, false, true);
      } catch (error) { console.error(error); }
    },
    async getTotalTeam() {
      try {
        this.total_sold_team = await this.getTotalInfo(this.selectedMovie.name, true, false, true);
      } catch (error) { console.error(error); }
    },
    async getTotalWithoutPfand() {
      try {
        this.total_sold_without_pfand = await this.getTotalInfo(this.selectedMovie.name, false, false, false);
      } catch (error) { console.error(error); }
    },
    async getTickets() {
      try {
        this.tickets_sold = await this.getTicketInfo(this.selectedMovie.name, false, true);
      } catch (error) { console.error(error); }
    },
    async getTicketsTotal() {
      try {
        this.tickets_total = await this.getTicketInfo(this.selectedMovie.name, false, false);
      } catch (error) { console.error(error); }
    },
    async getTotalInfo(movie, isteam, cancellation, pfand) {
      try {
        const response = await axios.get(
          `/api/v1/history/total?movie=${movie}&isteam=${isteam}&cancellation=${cancellation}&pfand=${pfand}`,
          { withCredentials: false }
        );
        return response.data;
      } catch (error) { console.error(error); }
    },
    async getTicketInfo(movie, isteam, freeticket) {
      try {
        const response = await axios.get(
          `/api/v1/history/tickets?movie=${movie}&isteam=${isteam}&freeticket=${freeticket}`,
          { withCredentials: false }
        );
        return response.data;
      } catch (error) { console.error(error); }
    },
    async setSelectedMovie() {
      await this.getHistory();
      this.getHistoryProducts();
      await Promise.all([
        this.getTotal(),
        this.getTotalTeam(),
        this.getTotalWithoutPfand(),
        this.getTickets(),
        this.getTicketsTotal(),
      ]);
    },
  },
  created() {
    this.getMovies();
  },
  watch: {
    selectedMovie(newMovie, oldMovie) {
      if (newMovie !== oldMovie && newMovie) {
        this.setSelectedMovie();
      }
    },
  },
};
</script>

<style scoped>
.info-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px 0;
}
.info-row:not(:last-child) {
  border-bottom: 1px solid rgba(255, 255, 255, 0.04);
}
.stat-card {
  transition: transform 0.15s ease;
}
.stat-card:hover {
  transform: translateY(-2px);
}
</style>

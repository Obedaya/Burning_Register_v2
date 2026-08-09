<template>
  <v-container fluid class="pa-4 pa-md-6">
    <!-- Tabs for Admin sections -->
    <v-tabs v-model="activeTab" color="primary" class="mb-4">
      <v-tab value="orders">
        <v-icon start>mdi-receipt-text</v-icon>
        Orders
      </v-tab>
      <v-tab value="movies">
        <v-icon start>mdi-movie</v-icon>
        Movies
      </v-tab>
      <v-tab value="inventory">
        <v-icon start>mdi-package-variant</v-icon>
        Products
      </v-tab>
    </v-tabs>

    <!-- Movie selection (shared across tabs) -->
    <v-row dense class="mb-4" v-if="activeTab !== 'inventory'">
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

    <!-- ORDERS TAB -->
    <v-window v-model="activeTab">
      <v-window-item value="orders">
        <v-row dense v-if="selectedMovie">
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

              <v-divider class="my-4" />

              <v-btn
                block
                color="success"
                variant="tonal"
                class="mb-2"
                @click="downloadReport"
                prepend-icon="mdi-download"
              >
                Download Report
              </v-btn>
            </v-card>
          </v-col>

          <v-col cols="12" md="8">
            <v-card color="surface" class="mb-3" style="border: 1px solid rgba(255,255,255,0.06);">
              <v-card-title class="d-flex align-center justify-space-between pa-4">
                <div class="d-flex align-center">
                  <v-icon class="mr-2" size="20">mdi-receipt</v-icon>
                  <span class="font-weight-bold">Orders</span>
                </div>
                <v-chip size="small" color="primary" variant="tonal">{{ orders.length }}</v-chip>
              </v-card-title>
              <v-divider />
              <v-list density="compact" class="pa-1 overflow-y-auto" style="max-height: 320px;" bg-color="transparent">
                <v-list-item
                  v-for="(order, index) in orders"
                  :key="index"
                  @click="selectOrder(order)"
                  :active="selectedOrder === order"
                  active-color="error"
                  rounded="lg"
                  class="mx-1 my-1"
                >
                  <template v-slot:prepend>
                    <v-avatar size="32" :color="order.isteam ? 'success' : 'surface-variant'" variant="tonal">
                      <v-icon size="16">{{ order.isteam ? 'mdi-account-group' : 'mdi-account' }}</v-icon>
                    </v-avatar>
                  </template>
                  <v-list-item-title class="text-body-2 font-weight-medium">
                    {{ formatDateTime(order.timestamp) }}
                  </v-list-item-title>
                  <v-list-item-subtitle class="text-caption">
                    {{ printProducts(order) }}
                  </v-list-item-subtitle>
                  <template v-slot:append>
                    <v-chip size="x-small" color="primary" variant="tonal">{{ formatPrice(order.total) }}</v-chip>
                  </template>
                </v-list-item>
              </v-list>
            </v-card>

            <v-btn
              v-if="selectedOrder"
              color="error"
              variant="tonal"
              @click="cancelSelectedOrder"
              prepend-icon="mdi-cancel"
              class="mb-3"
            >
              Cancel Selected Order
            </v-btn>

            <v-card color="surface" style="border: 1px solid rgba(255,255,255,0.06);">
              <v-card-title class="d-flex align-center justify-space-between pa-4">
                <div class="d-flex align-center">
                  <v-icon class="mr-2" size="20" color="error">mdi-cancel</v-icon>
                  <span class="font-weight-bold">Cancelled Orders</span>
                </div>
                <v-chip size="small" color="error" variant="tonal">{{ cancelled_orders.length }}</v-chip>
              </v-card-title>
              <v-divider />
              <v-list density="compact" class="pa-1 overflow-y-auto" style="max-height: 180px;" bg-color="transparent">
                <v-list-item
                  v-for="(order, index) in cancelled_orders"
                  :key="index"
                  rounded="lg"
                  class="mx-1 my-1"
                >
                  <v-list-item-title class="text-body-2 text-medium-emphasis">
                    {{ formatDateTime(order.timestamp) }}
                  </v-list-item-title>
                  <v-list-item-subtitle class="text-caption">
                    {{ printProducts(order) }} — {{ formatPrice(order.total) }}
                  </v-list-item-subtitle>
                </v-list-item>
                <v-list-item v-if="cancelled_orders.length === 0" class="text-center text-caption text-medium-emphasis pa-4">
                  No cancelled orders
                </v-list-item>
              </v-list>
            </v-card>
          </v-col>
        </v-row>

        <v-card v-else color="surface" class="pa-12 text-center" style="border: 1px solid rgba(255,255,255,0.06);">
          <v-icon size="64" color="surface-variant" class="mb-4">mdi-movie-open-outline</v-icon>
          <div class="text-h6 text-medium-emphasis">Select a movie to manage orders</div>
        </v-card>
      </v-window-item>

      <!-- MOVIES TAB -->
      <v-window-item value="movies">
        <v-row dense>
          <v-col cols="12" md="6">
            <v-card color="surface" class="pa-5" style="border: 1px solid rgba(255,255,255,0.06);">
              <div class="text-h6 font-weight-bold mb-4">
                {{ movieEditing ? 'Edit Movie' : 'Add New Movie' }}
              </div>
              <v-text-field label="Movie Name" v-model="tempMovieName" class="mb-2" />
              <v-text-field label="Room" v-model="tempMovieRoom" class="mb-2" />
              <v-text-field
                label="Date and Time"
                v-model="tempMovieDatetime"
                :rules="movieDatetimeRule"
                :disabled="datetimeDisabled"
                hint="Format: YYYY-MM-DD HH:MM:SS"
                class="mb-2"
              />
              <v-text-field label="Trailer URL" v-model="tempMovieTrailer" class="mb-2" />
              <v-text-field label="Description" v-model="tempMovieDescription" class="mb-2" />
              <v-text-field label="Language" v-model="tempMovieLanguage" class="mb-2" />
              <v-text-field label="Poster URL" v-model="tempMoviePoster" class="mb-2" />
              <v-text-field label="Stripe Payment" v-model="tempMovieStripePayment" class="mb-2" />

              <div class="d-flex ga-2 mt-2">
                <v-btn color="primary" @click="submitMovie" prepend-icon="mdi-check">
                  {{ movieEditing ? 'Update' : 'Add' }}
                </v-btn>
                <v-btn variant="tonal" @click="clearForm" prepend-icon="mdi-close">Cancel</v-btn>
              </div>
            </v-card>
          </v-col>
          <v-col cols="12" md="6">
            <v-card color="surface" style="border: 1px solid rgba(255,255,255,0.06);">
              <v-card-title class="d-flex align-center pa-4">
                <v-icon class="mr-2" size="20">mdi-movie-roll</v-icon>
                <span class="font-weight-bold">All Movies</span>
              </v-card-title>
              <v-divider />
              <v-list density="compact" class="pa-1 overflow-y-auto" style="max-height: 500px;" bg-color="transparent">
                <v-list-item
                  v-for="(movie, index) in movies"
                  :key="index"
                  rounded="lg"
                  class="mx-1 my-1"
                >
                  <v-list-item-title class="text-body-2 font-weight-medium">{{ movie.name }}</v-list-item-title>
                  <v-list-item-subtitle class="text-caption">
                    {{ movie.room }} — {{ formatDate(movie.datetime) }}
                  </v-list-item-subtitle>
                  <template v-slot:append>
                    <v-btn icon size="small" variant="text" color="secondary" @click="editMovieFromList(movie)">
                      <v-icon size="18">mdi-pencil</v-icon>
                    </v-btn>
                    <v-btn icon size="small" variant="text" color="error" @click="confirmDeleteMovie(movie)">
                      <v-icon size="18">mdi-delete</v-icon>
                    </v-btn>
                  </template>
                </v-list-item>
              </v-list>
            </v-card>
          </v-col>
        </v-row>
      </v-window-item>

      <!-- INVENTORY TAB -->
      <v-window-item value="inventory">
        <v-row dense>
          <v-col cols="12" md="5">
            <v-card color="surface" class="pa-5" style="border: 1px solid rgba(255,255,255,0.06);">
              <div class="text-h6 font-weight-bold mb-4">
                {{ productEditing ? 'Edit Product' : 'Add New Product' }}
              </div>
              <v-text-field label="Product Name" v-model="tempProductName" class="mb-2" />
              <v-select
                label="Category"
                v-model="tempProductCategory"
                :items="categories"
                class="mb-2"
              />
              <v-text-field
                label="Price (€)"
                v-model.number="tempProductPrice"
                type="number"
                step="0.01"
                min="0"
                class="mb-2"
              />
              <v-text-field
                label="Team Price (€)"
                v-model.number="tempProductPriceTeam"
                type="number"
                step="0.01"
                min="0"
                class="mb-2"
              />
              <v-text-field
                label="Stock Amount"
                v-model.number="tempProductAmount"
                type="number"
                min="0"
                class="mb-2"
              />

              <div class="d-flex ga-2 mt-2">
                <v-btn color="primary" @click="submitProduct" prepend-icon="mdi-check">
                  {{ productEditing ? 'Update' : 'Add' }}
                </v-btn>
                <v-btn variant="tonal" @click="clearProductForm" prepend-icon="mdi-close">Cancel</v-btn>
              </div>
            </v-card>
          </v-col>

          <v-col cols="12" md="7">
            <v-card color="surface" style="border: 1px solid rgba(255,255,255,0.06);">
              <v-card-title class="d-flex align-center justify-space-between pa-4">
                <div class="d-flex align-center">
                  <v-icon class="mr-2" size="20">mdi-package-variant</v-icon>
                  <span class="font-weight-bold">Products</span>
                </div>
                <v-chip size="small" color="primary" variant="tonal">{{ inventoryItems.length }}</v-chip>
              </v-card-title>
              <v-divider />
              <v-table density="comfortable" hover>
                <thead>
                  <tr>
                    <th>Name</th>
                    <th>Category</th>
                    <th class="text-right">Price</th>
                    <th class="text-right">Team Price</th>
                    <th class="text-center">Stock</th>
                    <th class="text-center">Sold</th>
                    <th class="text-center">Actions</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="item in inventoryItems" :key="item._id">
                    <td class="font-weight-medium">{{ item.name }}</td>
                    <td>
                      <v-chip size="x-small" variant="tonal" :color="getCategoryColor(item.category)">
                        {{ item.category }}
                      </v-chip>
                    </td>
                    <td class="text-right">{{ formatPrice(item.price) }}</td>
                    <td class="text-right">{{ formatPrice(item.price_team) }}</td>
                    <td class="text-center">{{ item.amount }}</td>
                    <td class="text-center">{{ item.amount_sold }}</td>
                    <td class="text-center">
                      <v-btn icon size="small" variant="text" color="secondary" @click="editProduct(item)">
                        <v-icon size="18">mdi-pencil</v-icon>
                      </v-btn>
                      <v-btn icon size="small" variant="text" color="error" @click="confirmDeleteProduct(item)">
                        <v-icon size="18">mdi-delete</v-icon>
                      </v-btn>
                    </td>
                  </tr>
                </tbody>
              </v-table>
            </v-card>
          </v-col>
        </v-row>
      </v-window-item>
    </v-window>

    <!-- Delete confirmation dialog -->
    <v-dialog v-model="deleteDialog" max-width="400">
      <v-card color="surface" class="pa-4">
        <v-card-title class="text-h6">Confirm Deletion</v-card-title>
        <v-card-text>
          Are you sure you want to delete <strong>{{ deleteTargetName }}</strong>? This action cannot be undone.
        </v-card-text>
        <v-card-actions>
          <v-spacer />
          <v-btn variant="tonal" @click="deleteDialog = false">Cancel</v-btn>
          <v-btn color="error" @click="executeDelete">Delete</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <v-snackbar v-model="snackbar" :color="snackbarColor" timeout="3000" location="bottom right">
      {{ snackbarText }}
    </v-snackbar>
  </v-container>
</template>

<script>
import axios from "axios";
import { useMovieStore } from "@/stores/movieStore";
import { ref, watch } from "vue";

export default {
  data() {
    return {
      activeTab: 'orders',
      movies: [],
      orders: [],
      cancelled_orders: [],
      selectedOrder: null,
      inventoryItems: [],
      categories: ['Drinks', 'Snacks', 'Sweets', 'Tickets', 'Pfand'],

      // Movie form
      tempMovieName: "",
      tempMovieRoom: "",
      tempMovieDatetime: new Date().toISOString().slice(0, 19).replace('T', ' '),
      movieDatetimeRule: [
        value => {
          if (/^(19|20)\d\d-(0[1-9]|1[012])-(0[1-9]|[12][0-9]|3[01]) ([01][0-9]|2[0-3]):([0-5][0-9]):([0-5][0-9])$/.test(value)) return true
          return 'Format: YYYY-MM-DD HH:MM:SS'
        },
      ],
      tempMovieTrailer: "",
      tempMovieDescription: "",
      tempMovieLanguage: "",
      tempMoviePoster: "",
      tempMovieStripePayment: "",
      movieEditing: false,
      editingMovieId: null,
      datetimeDisabled: false,

      // Product form
      tempProductName: "",
      tempProductCategory: "Drinks",
      tempProductPrice: 0,
      tempProductPriceTeam: 0,
      tempProductAmount: 0,
      productEditing: false,
      editingProductId: null,

      // Delete dialog
      deleteDialog: false,
      deleteTargetName: "",
      deleteTargetType: null,
      deleteTargetId: null,

      // Snackbar
      snackbar: false,
      snackbarText: "",
      snackbarColor: "success",
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
    formatDateTime(timestamp) {
      if (!timestamp) return '';
      const d = new Date(timestamp);
      return d.toLocaleDateString('de-DE', { day: '2-digit', month: '2-digit', year: 'numeric', hour: '2-digit', minute: '2-digit', second: '2-digit' });
    },
    getCategoryColor(category) {
      const colors = { 'Drinks': 'info', 'Snacks': 'warning', 'Sweets': 'error', 'Tickets': 'success', 'Pfand': 'secondary' };
      return colors[category] || 'primary';
    },
    showSnackbar(text, color = 'success') {
      this.snackbarText = text;
      this.snackbarColor = color;
      this.snackbar = true;
    },

    // Data fetching
    async getMovies() {
      try {
        const response = await axios.get("/api/v1/movies/", { withCredentials: false });
        this.movies = response.data;
      } catch (error) { console.log(error); }
    },
    async getHistory() {
      if (!this.selectedMovie) return;
      try {
        const response = await axios.get("/api/v1/history/?movie=" + this.selectedMovie.name + "&cancellation=false", { withCredentials: false });
        this.orders = response.data;
      } catch (error) { console.log(error); }
    },
    async getHistoryCancelled() {
      if (!this.selectedMovie) return;
      try {
        const response = await axios.get("/api/v1/history/?movie=" + this.selectedMovie.name + "&cancellation=true", { withCredentials: false });
        this.cancelled_orders = response.data;
      } catch (error) { console.log(error); }
    },
    async getInventory() {
      try {
        const response = await axios.get("/api/v1/inventory/", { withCredentials: false });
        this.inventoryItems = response.data;
      } catch (error) { console.log(error); }
    },

    // Orders
    selectOrder(order) {
      this.selectedOrder = this.selectedOrder === order ? null : order;
    },
    async cancelSelectedOrder() {
      try {
        await axios.post("/api/v1/history/cancel/?_id=" + this.selectedOrder._id.toString(), { withCredentials: false });
        this.showSnackbar("Order cancelled successfully");
        this.selectedOrder = null;
        await this.getHistory();
        await this.getHistoryCancelled();
      } catch (error) {
        this.showSnackbar("Failed to cancel order", "error");
        console.log(error);
      }
    },

    // Download Report
    downloadReport() {
      if (!this.selectedMovie) {
        this.showSnackbar("Please select a movie first", "warning");
        return;
      }
      axios
        .get('/api/v1/report/report?movie=' + this.selectedMovie.name, {
          responseType: 'blob',
          withCredentials: false,
        })
        .then((response) => {
          const url = window.URL.createObjectURL(new Blob([response.data]));
          const link = document.createElement('a');
          link.href = url;
          link.setAttribute('download', this.selectedMovie.name + '.xlsx');
          document.body.appendChild(link);
          link.click();
          link.parentNode.removeChild(link);
          this.showSnackbar("Report downloaded!");
        })
        .catch((error) => {
          this.showSnackbar("Failed to download report", "error");
          console.error(error);
        });
    },

    // Movie CRUD
    submitMovie() {
      if (!this.tempMovieName.trim()) {
        this.showSnackbar("Please enter a movie name", "warning");
        return;
      }
      if (!this.tempMovieRoom.trim()) {
        this.showSnackbar("Please enter a room", "warning");
        return;
      }
      if (this.movieEditing) {
        this.editMovieToDB();
      } else {
        this.addMovieToDB();
      }
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
      this.editingMovieId = null;
      this.datetimeDisabled = false;
    },
    async addMovieToDB() {
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
      try {
        await axios.post("/api/v1/movies/", movie, { withCredentials: false });
        this.showSnackbar("Movie added successfully");
        this.clearForm();
        await this.getMovies();
      } catch (error) {
        this.showSnackbar("Failed to add movie", "error");
        console.log(error);
      }
    },
    editMovieFromList(movie) {
      this.movieEditing = true;
      this.editingMovieId = movie._id;
      this.datetimeDisabled = true;
      let datetime = new Date(movie.datetime);
      this.tempMovieName = movie.name;
      this.tempMovieRoom = movie.room;
      this.tempMovieDatetime = datetime.toISOString().slice(0, 19).replace('T', ' ');
      this.tempMovieTrailer = movie.trailer || "";
      this.tempMovieDescription = movie.description || "";
      this.tempMovieLanguage = movie.language || "";
      this.tempMoviePoster = movie.poster || "";
      this.tempMovieStripePayment = movie.stripe_payment || "";
      this.activeTab = 'movies';
    },
    async editMovieToDB() {
      const movie = {
        name: this.tempMovieName,
        room: this.tempMovieRoom,
        trailer: this.tempMovieTrailer,
        description: this.tempMovieDescription,
        language: this.tempMovieLanguage,
        poster: this.tempMoviePoster,
        stripe_payment: this.tempMovieStripePayment,
      };
      try {
        await axios.put("/api/v1/movies/" + this.editingMovieId, movie, { withCredentials: false });
        this.showSnackbar("Movie updated successfully");
        this.clearForm();
        await this.getMovies();
      } catch (error) {
        this.showSnackbar("Failed to update movie", "error");
        console.log(error);
      }
    },
    confirmDeleteMovie(movie) {
      this.deleteTargetName = movie.name;
      this.deleteTargetType = 'movie';
      this.deleteTargetId = movie._id;
      this.deleteDialog = true;
    },

    // Product CRUD
    clearProductForm() {
      this.tempProductName = "";
      this.tempProductCategory = "Drinks";
      this.tempProductPrice = 0;
      this.tempProductPriceTeam = 0;
      this.tempProductAmount = 0;
      this.productEditing = false;
      this.editingProductId = null;
    },
    async submitProduct() {
      if (!this.tempProductName.trim()) {
        this.showSnackbar("Please enter a product name", "warning");
        return;
      }
      if (this.tempProductPrice <= 0) {
        this.showSnackbar("Price must be greater than 0", "warning");
        return;
      }
      if (this.productEditing) {
        await this.updateProduct();
      } else {
        await this.addProduct();
      }
    },
    async addProduct() {
      const product = {
        name: this.tempProductName,
        category: this.tempProductCategory,
        price: this.tempProductPrice,
        price_team: this.tempProductPriceTeam,
        amount: this.tempProductAmount,
        amount_sold: 0,
      };
      try {
        await axios.post("/api/v1/inventory/", product, { withCredentials: false });
        this.showSnackbar("Product added successfully");
        this.clearProductForm();
        await this.getInventory();
      } catch (error) {
        this.showSnackbar("Failed to add product", "error");
        console.log(error);
      }
    },
    editProduct(item) {
      this.productEditing = true;
      this.editingProductId = item._id;
      this.tempProductName = item.name;
      this.tempProductCategory = item.category;
      this.tempProductPrice = item.price;
      this.tempProductPriceTeam = item.price_team;
      this.tempProductAmount = item.amount;
    },
    async updateProduct() {
      const product = {
        name: this.tempProductName,
        category: this.tempProductCategory,
        price: this.tempProductPrice,
        price_team: this.tempProductPriceTeam,
        amount: this.tempProductAmount,
      };
      try {
        await axios.put("/api/v1/inventory/" + this.editingProductId, product, { withCredentials: false });
        this.showSnackbar("Product updated successfully");
        this.clearProductForm();
        await this.getInventory();
      } catch (error) {
        this.showSnackbar("Failed to update product", "error");
        console.log(error);
      }
    },
    confirmDeleteProduct(item) {
      this.deleteTargetName = item.name;
      this.deleteTargetType = 'product';
      this.deleteTargetId = item._id;
      this.deleteDialog = true;
    },

    // Generic delete
    async executeDelete() {
      try {
        if (this.deleteTargetType === 'product') {
          await axios.delete("/api/v1/inventory/" + this.deleteTargetId, { withCredentials: false });
          this.showSnackbar("Product deleted");
          await this.getInventory();
        } else if (this.deleteTargetType === 'movie') {
          await axios.delete("/api/v1/movies/" + this.deleteTargetId, { withCredentials: false });
          this.showSnackbar("Movie deleted");
          await this.getMovies();
        }
      } catch (error) {
        this.showSnackbar("Failed to delete", "error");
        console.log(error);
      }
      this.deleteDialog = false;
    },

    printProducts(order) {
      return order.products.map(p => `${p.name} x${p.amount}`).join(", ");
    },
  },
  created() {
    this.getMovies();
    this.getInventory();
    if (this.selectedMovie) {
      this.getHistory();
      this.getHistoryCancelled();
    }
  },
  watch: {
    selectedMovie() {
      if (this.selectedMovie) {
        this.getHistory();
        this.getHistoryCancelled();
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
</style>

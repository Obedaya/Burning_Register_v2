<template>
  <v-container fluid class="pa-4 pa-md-6">
    <v-row dense class="mb-4">
      <v-col cols="12" md="8">
        <v-select
          v-model="selectedMovie"
          :items="movies"
          item-title="name"
          item-value="_id"
          label="Select a movie"
          return-object
          prepend-inner-icon="mdi-movie-open"
          hide-details
          class="movie-select"
        />
      </v-col>
      <v-col cols="12" md="4" class="d-flex align-center">
        <v-chip
          v-if="selectedMovie"
          color="secondary"
          variant="tonal"
          size="small"
          class="mr-2"
        >
          <v-icon start size="14">mdi-door</v-icon>
          {{ selectedMovie.room }}
        </v-chip>
        <v-chip
          v-if="selectedMovie"
          color="info"
          variant="tonal"
          size="small"
        >
          <v-icon start size="14">mdi-calendar</v-icon>
          {{ formatDate(selectedMovie.datetime) }}
        </v-chip>
      </v-col>
    </v-row>

    <v-row>
      <v-col cols="12" md="7" lg="8">
        <ButtonPanel
          :products="products"
          @addItem="addItem"
          :visible="buttonPanelvisible"
          v-if="buttonPanelvisible"
        />
        <PayPanel
          :total="total"
          :amountKeyboard="amountKeyboard"
          :movieselected="selectedMovie !== null"
          @checkout="checkout"
          @goBack="changeView"
          v-else
        />
      </v-col>

      <v-col cols="12" md="5" lg="4">
        <RegisterCart
          ref="registerCart"
          :amountKeyboard="amountKeyboard"
          :productsinCart="productsinCart"
          :isteam="isteam"
          @selectProduct="selectProduct"
          @total="setTotal"
          class="mb-3"
        />
        <RegisterKeypad
          @keyboard="keyboardValue"
          @clearCart="clearCart"
          @toggleTeam="toggleTeam"
          @changeView="changeView"
          @deleteFromCart="deleteFromCart"
          @increaseProductAmount="increaseProductAmount"
          @decreaseProductAmount="decreaseProductAmount"
          :isTeamActive="isteam"
          v-if="buttonPanelvisible"
        />
      </v-col>
    </v-row>

    <v-snackbar v-model="snackbar" :color="snackbarColor" timeout="2000" location="bottom right">
      {{ snackbarText }}
    </v-snackbar>
  </v-container>
</template>

<script>
import ButtonPanel from "../components/ButtonPanel.vue";
import RegisterCart from "../components/RegisterCart.vue";
import RegisterKeypad from "../components/RegisterKeypad.vue";
import PayPanel from "../components/PayPanel.vue";
import axios from "axios";
import { useMovieStore } from "@/stores/movieStore";
import { ref, watch } from "vue";

export default {
  data() {
    return {
      products: [],
      amountKeyboard: "",
      productsinCart: [],
      isteam: false,
      buttonPanelvisible: true,
      total: 0,
      movies: [],
      selectedProduct: null,
      snackbar: false,
      snackbarText: "",
      snackbarColor: "success",
    };
  },
  mounted() {
    this.getproducts();
    this.getMovies();
  },
  setup() {
    const movieStore = useMovieStore();
    const selectedMovie = ref(movieStore.selectedMovie);

    watch(selectedMovie, (newVal) => {
      movieStore.selectMovie(newVal);
    });

    return { selectedMovie };
  },
  components: { ButtonPanel, RegisterCart, RegisterKeypad, PayPanel },
  methods: {
    getproducts() {
      axios
        .get("/api/v1/inventory/", { withCredentials: false })
        .then((response) => { this.products = response.data; })
        .catch((error) => { console.log(error); });
    },
    keyboardValue(keyboardValue) {
      if (keyboardValue === "delete") {
        this.amountKeyboard = this.amountKeyboard.toString().slice(0, -1);
      } else if (keyboardValue === "00") {
        this.amountKeyboard /= 10;
      } else {
        this.amountKeyboard += keyboardValue;
      }
      this.amountKeyboard = this.amountKeyboard.toString();
      this.amountKeyboard = this.amountKeyboard.replace(/\.$/, "");
      this.amountKeyboard = this.amountKeyboard.replace(/^0+(?=\d)/, "");
    },
    addItem(item) {
      const product = this.productsinCart.find((p) => p.name === item.name);
      if (this.amountKeyboard === "") {
        this.amountKeyboard = "1";
      } else if (this.amountKeyboard === "0") {
        return;
      }
      if (product) {
        product.amount += +this.amountKeyboard;
      } else {
        this.productsinCart.push({
          name: item.name,
          price: this.isteam ? item.price_team : item.price,
          amount: +this.amountKeyboard,
          category: item.category,
        });
      }
      if (item.category === "Drinks" && item.name !== "Pfand" && !this.isteam) {
        this.addItem(this.products.find((p) => p.name === "Pfand"));
      }
      this.amountKeyboard = "";
    },
    clearCart() {
      this.productsinCart = [];
    },
    toggleTeam() {
      if (this.isteam) {
        this.isteam = !this.isteam;
        this.productsinCart.forEach((product) => {
          product.price = this.products.find(
            (p) => p.name === product.name
          ).price;
          if (product.category === "Drinks") {
            this.amountKeyboard = product.amount;
            this.addItem(this.products.find((p) => p.name === "Pfand"));
          }
        });
      } else {
        this.isteam = !this.isteam;
        this.productsinCart.forEach((product) => {
          product.price = this.products.find(
            (p) => p.name === product.name
          ).price_team;
        });
        this.productsinCart.forEach((product) => {
          if (product.name === "Pfand") {
            this.productsinCart.splice(
              this.productsinCart.findIndex((p) => p.name === "Pfand"),
              1
            );
          }
        });
      }
    },
    changeView() {
      if (this.buttonPanelvisible) {
        if (!this.selectedMovie) {
          this.showSnackbar("Please select a movie first", "warning");
          return;
        }
        if (this.productsinCart.length === 0) {
          this.showSnackbar("Cart is empty — add items first", "warning");
          return;
        }
      }
      this.buttonPanelvisible = !this.buttonPanelvisible;
      this.amountKeyboard = "";
    },
    setTotal(total) {
      this.total = total;
    },
    checkout() {
      const order = {
        timestamp: new Date().toISOString(),
        total: this.total,
        isteam: this.isteam,
        movie: this.selectedMovie.name,
        cancellation: false,
        products: this.productsinCart,
      };
      axios
        .post("/api/v1/history/", order, { withCredentials: false })
        .then(() => {
          this.showSnackbar("Order placed successfully!", "success");
        })
        .catch((error) => {
          this.showSnackbar("Failed to place order", "error");
          console.log(error);
        });
      this.clearCart();
      this.amountKeyboard = "";
      this.total = 0;
      this.isteam = false;
      this.changeView();
    },
    getMovies() {
      axios
        .get("/api/v1/movies/", { withCredentials: false })
        .then((response) => { this.movies = response.data; })
        .catch((error) => { console.log(error); });
    },
    selectProduct(product) {
      this.selectedProduct = product;
    },
    deleteFromCart() {
      if (this.selectedProduct) {
        this.productsinCart.splice(
          this.productsinCart.findIndex(
            (p) => p.name === this.selectedProduct.name
          ),
          1
        );
        this.selectedProduct = null;
        this.$refs.registerCart.clearSelection();
      }
    },
    increaseProductAmount() {
      if (this.selectedProduct) {
        this.selectedProduct.amount += 1;
      }
    },
    decreaseProductAmount() {
      if (this.selectedProduct) {
        if (
          this.selectedProduct.category === "Drinks" &&
          this.selectedProduct.name !== "Pfand" &&
          !this.isteam
        ) {
          const pfand = this.productsinCart.find((p) => p.name === "Pfand");
          if (pfand) {
            pfand.amount -= 1;
            if (pfand.amount === 0) {
              this.productsinCart.splice(
                this.productsinCart.findIndex((p) => p.name === "Pfand"),
                1
              );
            }
          }
        }
        this.selectedProduct.amount -= 1;
        if (this.selectedProduct.amount === 0) {
          this.deleteFromCart();
        }
      }
    },
    showSnackbar(text, color) {
      this.snackbarText = text;
      this.snackbarColor = color;
      this.snackbar = true;
    },
    formatDate(datetime) {
      if (!datetime) return '';
      const d = new Date(datetime);
      return d.toLocaleDateString('de-DE', { day: '2-digit', month: '2-digit', year: 'numeric', hour: '2-digit', minute: '2-digit' });
    },
  },
};
</script>

<style scoped>
.movie-select {
  max-width: 100%;
}
</style>

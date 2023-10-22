<template>
  <v-container fluid>
    <v-row>
      <v-col>
        <v-select
          v-model="selectedMovie"
          :items="movies"
          item-title="name"
          item-value="_id"
          label="Select a movie"
          return-object
        ></v-select>
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
          v-else
        />
      </v-col>
    </v-row>
    <v-row>
      <v-col>
        <RegisterKeypad
          @keyboard="keyboardValue"
          @clearCart="clearCart"
          @toggleTeam="toggleTeam"
          @changeView="changeView"
          @deleteFromCart="deleteFromCart"
          @increaseProductAmount="increaseProductAmount"
          @decreaseProductAmount="decreaseProductAmount"
        />
      </v-col>
      <v-col>
        <RegisterCart
          ref="registerCart"
          :amountKeyboard="amountKeyboard"
          :productsinCart="productsinCart"
          :isteam="isteam"
          @selectProduct="selectProduct"
          @total="setTotal"
        />
      </v-col>
    </v-row>
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
    };
  },
  mounted() {
    this.getproducts();
    this.getMovies();
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

  components: {
    ButtonPanel,
    RegisterCart,
    RegisterKeypad,
    PayPanel,
  },
  methods: {
    getproducts() {
      axios
        .get("/api/v1/inventory/", {
          withCredentials: false, // Ensure credentials are not sent
        })
        .then((response) => {
          // Handle success
          console.log(response.data);
          this.products = response.data;
        })
        .catch((error) => {
          // Handle errors
          console.log(error);
        });
    },
    selectCategory(items) {
      this.productsinCart = items;
    },
    // Handle keypad input
    keyboardValue(keyboardValue) {
      if (keyboardValue === "delete") {
        this.amountKeyboard = this.amountKeyboard.toString().slice(0, -1);
      } else if (keyboardValue === "00") {
        this.amountKeyboard /= 10;
      } else {
        this.amountKeyboard += keyboardValue;
      }
      this.amountKeyboard = this.amountKeyboard.toString();
      // Remove trailing dot
      this.amountKeyboard = this.amountKeyboard.replace(/\.$/, "");
      // Remove leading zeros
      this.amountKeyboard = this.amountKeyboard.replace(/^0+(?=\d)/, "");
    },
    // Add item to cart
    addItem(item) {
      const product = this.productsinCart.find((p) => p.name === item.name);
      if (this.amountKeyboard === "") {
        this.amountKeyboard = "1";
      } else if (this.amountKeyboard === "0") {
        return;
      }
      if (product) {
        product.amount += parseInt(this.amountKeyboard);
      } else if (this.isteam) {
        this.productsinCart.push({
          name: item.name,
          price: item.price_team,
          amount: parseInt(this.amountKeyboard),
          category: item.category,
        });
      } else {
        this.productsinCart.push({
          name: item.name,
          price: item.price,
          amount: parseInt(this.amountKeyboard),
          category: item.category,
        });
      }
      // Automatically add Pfand if category is DRINK and item added is not Pfand
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
          // Add Pfand for every item amount in category Drinks
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
          // Remove Pfand from cart if Team is toggled on
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
      this.buttonPanelvisible = !this.buttonPanelvisible;
    },
    setTotal(total) {
      this.total = total;
    },
    // Checkout, clear cart and reset amountKeyboard
    checkout() {
      console.log(this.productsinCart);
      // Create new dictionary with selected movie, timestamp, list of products and total price
      const order = {
        timestamp: new Date().toISOString(),
        total: this.total,
        isteam: this.isteam,
        movie: this.selectedMovie.name,
        cancellation: false,
        products: this.productsinCart,
      };
      console.log(order);
      // Send order to backend
      axios
        .post("/api/v1/history/", order, {
          withCredentials: false, // Ensure credentials are not sent
        })
        .then((response) => {
          // Handle success
          console.log(response.data);
        })
        .catch((error) => {
          // Handle errors
          console.log(error);
        });
      this.clearCart();
      this.amountKeyboard = "";
      this.total = 0;
      this.isteam = false;
      this.changeView();
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
          // Check if Pfand is in cart
          if (this.productsinCart) {
            this.productsinCart.find((p) => p.name === "Pfand").amount -= 1;
          }
          if (
            this.productsinCart.find((p) => p.name === "Pfand").amount === 0
          ) {
            this.productsinCart.splice(
              this.productsinCart.findIndex((p) => p.name === "Pfand"),
              1
            );
          }
        }
        this.selectedProduct.amount -= 1;
        if (this.selectedProduct.amount === 0) {
          this.deleteFromCart();
        }
      }
    },
  },
};
</script>

<style>
.v-btn {
  margin: 5px;
  padding: 5px;
  width: 98%;
}
</style>

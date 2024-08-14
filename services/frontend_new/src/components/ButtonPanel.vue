<template>
  <v-row no-gutters>
    <v-col cols="2">
      <div class="category-button-background fill-height">
        <v-btn
          v-for="(cat, i) in getAllCategories(products, 'category')"
          :key="i"
          color="primary"
          @click="selectCategory(products, 'category', cat)"
        >
          {{ cat }}
        </v-btn>
      </div>
    </v-col>
    <v-col cols="10">
      <v-row>
        <v-col cols="4" v-for="(item, i) in selectedItems" :key="i">
          <v-btn
            color="secondary"
            @click="addItem(item)"
            class="product-button"
          >
            {{ item.name }}
          </v-btn>
        </v-col>
      </v-row>
    </v-col>
  </v-row>
</template>
  
  <script>
export default {
  data() {
    return {
      selectedItems: [],
    };
  },
  props: {
    products: {
      type: Array,
      default: () => [],
    },
    visible: {
      type: Boolean,
      default: true,
    },
  },
  methods: {
    addItem(item) {
      this.$emit("addItem", item);
    },
    selectCategory(list, key, value) {
      this.selectedItems = list.filter((item) => item[key] === value);
    },
    getAllCategories(list, categoryKey) {
      const categories = new Set();

      list.forEach((item) => {
        if (Object.prototype.hasOwnProperty.call(item, categoryKey)) {
          categories.add(item[categoryKey]);
        }
      });

      return Array.from(categories);
    },
  },
};
</script>
  
<style>
.product-button {
  margin: 5px; /* Adjust margin as needed for spacing */
}
</style>
  
import { create } from "zustand";
import type { Book } from "../types/book";

interface CartItem {
  book: Book;
  quantity: number;
}

interface CartState {
  items: CartItem[];
  addToCart: (book: Book) => void;
  removeFromCart: (bookId: number) => void;
  clearCart: () => void;
}

export const useCartStore = create<CartState>((set) => ({
  items: [],

  addToCart: (book) =>
    set((state) => {
      const existing = state.items.find(
        (item) => item.book.id === book.id,
      );

      if (existing) {
        return {
          items: state.items.map((item) =>
            item.book.id === book.id
              ? { ...item, quantity: item.quantity + 1 }
              : item,
          ),
        };
      }

      return {
        items: [...state.items, { book, quantity: 1 }],
      };
    }),

  removeFromCart: (bookId) =>
    set((state) => ({
      items: state.items.filter((item) => item.book.id !== bookId),
    })),

  clearCart: () => set({ items: [] }),
}));
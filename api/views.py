from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from .permissions import IsAdminOrReadOnly, IsOwnerOrReadOnly

from catalog.models import Book, Category
from orders.models import Order
from orders.cart import Cart

from .serializers import (
    BookSerializer,
    CategorySerializer,
    OrderSerializer,
    CartItemSerializer,
)
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.select_related('category').all()
    serializer_class = BookSerializer
    filterset_fields = ['category', 'author', 'stock']
    permission_classes = [IsAdminOrReadOnly]

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.prefetch_related('items__book').all()
    serializer_class = OrderSerializer
    filterset_fields = ['paid', 'email']
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class CartViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        cart = Cart(request)
        serializer = CartItemSerializer(list(cart), many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def add(self, request):
        cart = Cart(request)
        book = Book.objects.get(id=request.data.get('book_id'))
        cart.add(
            book=book,
            quantity=request.data.get('quantity', 1)
        )
        return Response({'status': 'book added to cart'})

    @action(detail=False, methods=['post'])
    def remove(self, request):
        cart = Cart(request)
        book = Book.objects.get(id=request.data.get('book_id'))
        cart.remove(book)
        return Response({'status': 'book removed from cart'})
    
    @action(detail=False, methods=['post'])
    def clear(self, request):
        cart = Cart(request)
        cart.clear()
        return Response({'status': 'cart cleared'})
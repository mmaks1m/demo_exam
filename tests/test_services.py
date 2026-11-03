# tests/test_services.py
# -*- coding: utf-8 -*-
import pytest
from unittest.mock import MagicMock, patch
import os
import sys

# Add project root to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from auth_service import AuthService
from product_service import ProductService
from order_service import OrderService

class TestAuthService:
    @patch('auth_service.get_db')
    def test_authenticate_success(self, mock_get_db):
        mock_session = MagicMock()
        mock_user = MagicMock()
        mock_user.login = 'admin'
        mock_user.password = 'admin123'
        mock_user.role = 'Администратор'
        mock_user.full_name = 'Администратор Системы'
        mock_session.query.return_value.filter.return_value.first.return_value = mock_user
        mock_get_db.return_value = iter([mock_session])

        user = AuthService.authenticate('admin', 'admin123')
        assert user is not None
        assert user.role == 'Администратор'

    @patch('auth_service.get_db')
    def test_authenticate_invalid_password(self, mock_get_db):
        mock_session = MagicMock()
        # First query (with login & password) returns None
        # Second query (with login only) returns user
        mock_existing_user = MagicMock(full_name='User', role='Клиент')
        mock_session.query.return_value.filter.return_value.first.side_effect = [None, mock_existing_user]
        mock_get_db.return_value = iter([mock_session])

        user = AuthService.authenticate('admin', 'wrong_pass')
        assert user is None

    @patch('auth_service.get_db')
    def test_authenticate_user_not_found(self, mock_get_db):
        mock_session = MagicMock()
        mock_session.query.return_value.filter.return_value.first.side_effect = [None, None]
        mock_get_db.return_value = iter([mock_session])

        user = AuthService.authenticate('nonexistent', 'pass')
        assert user is None

    @patch('auth_service.get_db')
    def test_get_user_by_id(self, mock_get_db):
        mock_session = MagicMock()
        mock_user = MagicMock()
        mock_user.id = 1
        mock_user.fio = 'Иванов И.И.'
        mock_session.query.return_value.filter.return_value.first.return_value = mock_user
        mock_get_db.return_value = iter([mock_session])

        user = AuthService.get_user_by_id(1)
        assert user is not None
        assert user.fio == 'Иванов И.И.'

class TestProductService:
    @patch('product_service.get_db')
    def test_get_all_products(self, mock_get_db):
        mock_session = MagicMock()
        mock_p1 = MagicMock(article='A1', name='Туфли')
        mock_p2 = MagicMock(article='A2', name='Ботинки')
        mock_session.query.return_value.all.return_value = [mock_p1, mock_p2]
        mock_get_db.return_value = iter([mock_session])

        products = ProductService.get_all_products()
        assert len(products) == 2

    @patch('product_service.get_db')
    def test_get_product_by_article(self, mock_get_db):
        mock_session = MagicMock()
        mock_p = MagicMock()
        mock_p.article = 'A123B4'
        mock_p.name = 'Кроссовки'
        mock_session.query.return_value.filter.return_value.first.return_value = mock_p
        mock_get_db.return_value = iter([mock_session])

        product = ProductService.get_product_by_article('A123B4')
        assert product is not None
        assert product.name == 'Кроссовки'

    @patch('product_service.get_db')
    def test_can_delete_product_false_when_in_orders(self, mock_get_db):
        mock_session = MagicMock()
        mock_session.query.return_value.filter.return_value.first.return_value = MagicMock()
        mock_get_db.return_value = iter([mock_session])

        can_delete = ProductService.can_delete_product('A123B4')
        assert can_delete is False

    @patch('product_service.get_db')
    def test_can_delete_product_true_when_no_orders(self, mock_get_db):
        mock_session = MagicMock()
        mock_session.query.return_value.filter.return_value.first.return_value = None
        mock_get_db.return_value = iter([mock_session])

        can_delete = ProductService.can_delete_product('A123B4')
        assert can_delete is True

class TestOrderService:
    @patch('order_service.get_db')
    def test_get_all_pickup_points(self, mock_get_db):
        mock_session = MagicMock()
        mock_pt1 = MagicMock(id=1, address='ул. Ленина 1')
        mock_session.query.return_value.order_by.return_value.all.return_value = [mock_pt1]
        mock_get_db.return_value = iter([mock_session])

        points = OrderService.get_all_pickup_points()
        assert len(points) == 1
        assert points[0].address == 'ул. Ленина 1'

    @patch('order_service.get_db')
    def test_delete_order_success(self, mock_get_db):
        mock_session = MagicMock()
        mock_order = MagicMock(id=10)
        mock_session.query.return_value.filter.return_value.first.return_value = mock_order
        mock_get_db.return_value = iter([mock_session])

        success, msg = OrderService.delete_order(10)
        assert success is True
        assert mock_session.commit.called

    @patch('order_service.get_db')
    def test_delete_order_not_found(self, mock_get_db):
        mock_session = MagicMock()
        mock_session.query.return_value.filter.return_value.first.return_value = None
        mock_get_db.return_value = iter([mock_session])

        success, msg = OrderService.delete_order(999)
        assert success is False

<h1 align="center">Ecommerce graphql application</h1

This repository contains code for a FastAPI application with various routers and queries implemented using the
Strawberry library. The code provides an API for managing products, orders, users, addresses, and other related
functionalities. It also includes middleware for handling CORS (Cross-Origin Resource Sharing) and an asynchronous
context manager for managing the lifespan of the application.

## :star2: Features

Blank for now...  

## :heavy_exclamation_mark: Requirements

1. Docker ( __>=23.0.4__ ) and docker compose plugin ( __>=2.18.1__ )
2. 2GB RAM
3. 5GB+ ROM

## :heavy_plus_sign: Installation

1. Clone the repository:

```bash
git clone https://github.com/kieled/ecommerce-backend.git
```

2. Rename `.env.example` to `.env` and change variables like you want
3. Run command to start project

```bash
docker compose up -d --build
```

4. To check logs use this command _[ Optional ]_:

```bash
docker compose logs -f api consumer inst payment
```

This will start the server on: __http://localhost:8000__

## :red_circle: Usage

1. FastAPI docs available on: __http://localhost:8000/docs__
2. GraphQL User Interface on: __http://localhost:8000/graphql__

## :diamond_shape_with_a_dot_inside: HTTP Endpoints

The following API endpoints are available:

#### Authentication

- __`POST /setup`__ - Endpoint for setting up the application (creates superuser account). Requires
  the `secret_key`, `username`, and `password` fields as form data. Accessible only with a valid `secret_key` (from env
  file).
- __`POST /instagram/auth`__ - Endpoint for authenticating with an Instagram account. Requires
  the `username`, `password`, and
  optional `verification_code` (If you receive code on the email or 2FA, just resend your request with this code again)
  and locale fields as form data. _[AdminOnly]_

#### Images

- __`POST /load-images`__ - Endpoint for loading images. Requires the images field as a form data list of files to be
  uploaded. _[AdminOnly]_
- __`GET /download/{product_id}`__ - Endpoint for downloading product images as a ZIP file. Requires the product_id path
  parameter. _[AdminOnly]_
- __`POST /upload-files/`__ - Endpoint for uploading temporary images. Requires the files field as a form data list of
  files to be uploaded. _[AdminOnly]_

## :large_blue_circle: GraphQL Endpoints

### GraphQL Queries

The following GraphQL queries are available:

- __`requisites`__ - Retrieves a list of requisites based on the type_id parameter. _[AdminOnly]_
- __`active_requisite`__ - Retrieves the active requisite based on the type_id parameter.
- __`orders`__ - Retrieves a list of orders with pagination support. _[AdminOnly]_
- __`order_detail`__ - Retrieves detailed information about a specific order. _[AdminOnly]_
- __`users`__ - Retrieves a list of users with pagination support. _[AdminOnly]_
- __`self`__ - Retrieves information about the current authenticated user.
- __`hash`__ - Generates a hash for a given password.
- __`location_search`__ - Retrieves information about a location based on a query.
- __`location_reverse`__ - Retrieves information about a location based on latitude and longitude.
- __`order_public_list`__ - Retrieves a list of public orders with pagination support.
- __`order_public_detail`__ - Retrieves detailed information about a specific public order.
- __`check_promo`__ - Checks the validity of a promo code.
- __`requisite_types`__ - Retrieves a list of requisite types.
- __`products`__ - Retrieves a list of products with pagination support. _[AdminOnly]_
- __`product_detail`__ - Retrieves detailed information about a specific product. _[AdminOnly]_
- __`fetch_product`__ - Parses product information from an Aliexpress URL. _[AdminOnly]_
- __`products_public`__ - Retrieves a list of public products with pagination support.
- __`public_detail`__ - Retrieves detailed information about a specific public product.
- __`product_categories`__ - Retrieves a list of product categories.

### GraphQL Mutations

The following GraphQL mutations are available:

- __`update_requisite`__ - This mutation updates the transactions information based on the provided payload.
  _[AdminOnly]_
- __`delete_requisite`__ - This mutation deletes a requisite by its ID. _[AdminOnly]_
- __`create_requisite`__ - This mutation creates a new requisite based on the provided payload. _[AdminOnly]_
- __`update_order`__ - This mutation updates the order information based on the provided order input. _[AdminOnly]_
- __`create_order`__ - This mutation creates a new order based on the provided payload, including an address, products,
  and promo
  information.
- __`login`__ - This mutation performs administrator authorization by taking a username and password as input.
- __`logout`__ - This mutation logs out the authenticated user.
- __`refresh`__ - This mutation refreshes the JSON Web Token (JWT) token for an authenticated user.
- __`telegram_login`__ - This mutation performs authorization for customers through a Telegram widget.
- __`confirm_transaction`__ - This mutation confirms a transaction by its associated order ID. _[AdminOnly]_
- __`create_requisite_type`__ - This mutation creates a new requisite type based on the provided payload.
  _[AdminOnly]_
- __`update_requisite_type`__ - This mutation updates a requisite type based on the provided payload. _[AdminOnly]_
- __`delete_requisite_type`__ - This mutation deletes a requisite type by its ID. _[AdminOnly]_
- __`create_product`__ - This mutation creates a new product based on the provided product input. _[AdminOnly]_
- __`update_product`__ - This mutation updates the product information based on the provided product input.
  _[AdminOnly]_
- __`delete_product`__ - This mutation deletes a product by its ID. _[AdminOnly]_
- __`update_product_category`__ - This mutation updates a product category based on the provided payload.
  _[AdminOnly]_
- __`create_product_category`__ - This mutation creates a new product category based on the provided payload.
  _[AdminOnly]_
- __`delete_product_category`__ - This mutation deletes a product category by its ID. _[AdminOnly]_

## :recycle: Dependencies

The main dependencies used in this code are:

- __`FastAPI`__ - A modern, fast (high-performance) web framework for building APIs with Python.
- __`Strawberry`__ - A GraphQL library for Python that aims to provide a straightforward and type-safe approach to
  building GraphQL APIs.
- __`aio-pika`__ - a wrapper for the `aiormq` for `asyncio` and humans.
- __`Uvicorn`__ - an ASGI web server implementation for Python.

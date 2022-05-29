import "./ProductPage.scss";
import React from "react";
import { Link } from "react-router-dom";

import Navbar from "../../components/Navbar";
import ProductInput from "../../components/ProductInput";
import image from "../../assets/mocks/product.jpg"

import { Button, Container, Divider, Image, Group } from "@mantine/core";

function template() {
  return (
    <div className="product-page">
      <Group>
        <Navbar />
        <Container className="product-content">
          <Group position="center" direction="column">
            <h1>{"{FILE NAME}"}</h1>
            <Group style={{ width: "100%" }}>
              <Image src={image} height="50vh" />
              <Divider sx={{ height: "50vh" }} orientation="vertical" />
              <ProductInput />
            </Group>
          </Group>
        </Container>
      </Group>

      <Link to="/home">
        <Button
          style={{
            position: "absolute",
            bottom: "5rem",
            right: "10rem"
          }}
        >
          Save
        </Button>
      </Link>
    </div>
  );
};

export default template;

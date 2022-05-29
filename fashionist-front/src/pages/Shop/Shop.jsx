import "./Shop.scss";
import React from "react";

import Navbar from "../../components/Navbar";

import { Group, Container } from "@mantine/core";

function template() {
  return (
    <div className="shop">
      <Group>
        <Navbar />
        <Container fluid className="shop-content">
          <h1>Shop</h1>
        </Container>
      </Group>
    </div>
  );
};

export default template;

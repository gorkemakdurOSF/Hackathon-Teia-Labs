import "./Home.scss";
import React from "react";

import Navbar from "../../components/Navbar";
import Product from "../../components/Product";
import SearchBar from "../../components/SearchBar";
import FloatingActionButton from "../../components/FloatingActionButton";

import { Grid, Group, Container } from "@mantine/core";

function template() {
  return (
    <div className="home">
      <Group>
        <Navbar />
        <Container fluid className="home-content">
          <Group className="content" direction="column">
            <h1 className="content-title">Home</h1>
            <SearchBar />
            <div className="content-content">
              <Grid>
                <Grid.Col span={3}><Product isLikeable /></Grid.Col>
                <Grid.Col span={3}><Product isLikeable liked /></Grid.Col>
                <Grid.Col span={3}><Product /></Grid.Col>
                <Grid.Col span={3}><Product isShoppable /></Grid.Col>
                <Grid.Col span={3}><Product isShoppable isLikeable /></Grid.Col>
              </Grid>
            </div>
          </Group>
        </Container>
      </Group>
      <FloatingActionButton />
    </div>
  );
};

export default template;

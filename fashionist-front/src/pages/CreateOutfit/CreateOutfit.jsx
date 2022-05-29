import "./CreateOutfit.scss";
import React, { useState } from "react";

import Navbar from "../../components/Navbar";
import Product from "../../components/Product";

import { Button, Container, Grid, Group } from "@mantine/core";
import { useNavigate } from "react-router-dom";

function CreateOutfit() {
  const [outfit, setOutfit] = useState([]);
  const navigate = useNavigate();

  const add = (clothing) => {
    outfit.push(clothing);
  };

  const remove = (clothing) => {
    const index = outfit.indexOf(clothing);
    outfit.splice(index, 1);
  };

  const save = () => {
    console.log(outfit);
    navigate('/home');
  };

  return (
    <div className="create-outfit">
      <Group>
        <Navbar />
        <Container className="outfit-content">
          <Group position="center" direction="column">
            <h1>Create Outfit</h1>
            <Grid>
              <Grid.Col span={3}>
                <Product id={0} isLikeable liked isSelectable add={add} remove={remove} />
              </Grid.Col>
              <Grid.Col span={3}>
                <Product id={1} isLikeable isSelectable add={add} remove={remove} />
              </Grid.Col>
              <Grid.Col span={3}>
                <Product id={2} isLikeable isSelectable add={add} remove={remove} />
              </Grid.Col>
              <Grid.Col span={3}>
                <Product id={3} isLikeable isSelectable add={add} remove={remove} />
              </Grid.Col>
            </Grid>
          </Group>
        </Container>
      </Group>

      <Button
        style={{
          position: "absolute",
          bottom: "5rem",
          right: "10rem",
        }}
        onClick={() => save()}
      >
        Create outfit
      </Button>
    </div>
  );
};

export default CreateOutfit;

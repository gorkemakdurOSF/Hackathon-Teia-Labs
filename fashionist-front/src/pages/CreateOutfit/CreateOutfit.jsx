import "./CreateOutfit.scss";
import React, { useState } from "react";

import Navbar from "../../components/Navbar";
import Product from "../../components/Product";
import clothesService from "../../services/Clothes";
import outfitService from "../../services/Outfit";


import { Button, Container, Grid, Group } from "@mantine/core";
import { useNavigate } from "react-router-dom";




function CreateOutfit() {

  const [clothes, setClothes] = useState([]);

  const [outfit, setOutfit] = useState([]);
  const navigate = useNavigate();

  React.useEffect(() => {
    clothesService.getAllClothes()
      .then((clothes) => {
        setClothes(clothes);
      });
  }, []);

  const add = (clothing) => {
    outfit.push(clothing);
    setOutfit(outfit);
  };

  const remove = (clothing) => {
    const index = outfit.indexOf(clothing);
    outfit.splice(index, 1);
    setOutfit(outfit);
  };

  const save = () => {
    if (outfit.length > 0) {
      outfitService.createOutfit(outfit, [])
        .then(() => {
          navigate('/home');
        });
    }
  };

  return (
    <div className="create-outfit">
      <Group>
        <Navbar />
        <Container className="outfit-content">
          <Group position="center" direction="column">
            <h1>Create Outfit</h1>
            <Grid>
              {
                clothes.map((clothing) => {
                  return (
                    <Grid.Col span={3}>
                      <Product
                        key={clothing._id}
                        id={clothing._id}
                        liked={clothing.isLiked}
                        url={clothing.url}
                        isLikeable
                        isSelectable
                        add={add}
                        remove={remove}
                      />
                    </Grid.Col>
                  )
                })
              }
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

import "./Product.scss";
import React from "react";

import image from "../../assets/mocks/product.jpg";
import ndImage from "../../assets/mocks/product-zoom.jpg";

import { Image, Group } from "@mantine/core";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faHeart as heartFull, faShoppingBag } from "@fortawesome/free-solid-svg-icons";
import { faHeart as heartEmpty } from "@fortawesome/free-regular-svg-icons";

function template(liked, hover, isHover, isLikeable, isShoppable, like) {
  return (
    <div className="product">
      <div className="product-icons">
        <Group className="icons" spacing="xs">
          {
            isShoppable
            && (
              <FontAwesomeIcon
                className="shop-icon icon"
                icon={faShoppingBag}
              />
            )
          }
          {
            isLikeable
            && (
              <FontAwesomeIcon
                className={`like-icon icon ${!liked ? "not-liked" : "liked"}`}
                icon={!liked ? heartEmpty : heartFull}
                onClick={like}
              />
            )
          }
        </Group>
      </div>
      <Image
        src={!isHover ? image : ndImage}
        alt="product image"
        className="product-image"
        onMouseEnter={() => hover(true)}
        onMouseLeave={() => hover(false)}
      />
    </div>
  );
};

export default template;

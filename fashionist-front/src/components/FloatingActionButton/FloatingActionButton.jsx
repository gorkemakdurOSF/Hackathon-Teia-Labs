import "./FloatingActionButton.scss";
import React, { useState } from "react";

import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faPlus } from "@fortawesome/free-solid-svg-icons";
import { Divider, Paper, Text, ThemeIcon, Tooltip, Transition } from "@mantine/core";
import { useClickOutside } from "@mantine/hooks";
import { Link } from "react-router-dom";

function FloatingActionButton() {
  const [isClick, click] = useState(false);
  const [isHover, hover] = useState(false);
  const clickOutsideRef = useClickOutside(() => setTimeout(() => click(false), 100));

  return (
    <>
      <div
        className="floating-action-button"
        onMouseEnter={() => hover(true)}
        onMouseLeave={() => hover(false)}
        onClick={() => click(!isClick)}
        ref={clickOutsideRef}
      >
        <Tooltip
          opened={isHover && !isClick}
          label="Add products or create outfits"
          position="left"
          withArrow
        >
          <ThemeIcon radius="xl" size="xl" color="dark">
            <FontAwesomeIcon icon={faPlus} />
          </ThemeIcon>
        </Tooltip>
      </div>
      <Transition mounted={isClick} transition="slide-right" duration={400} timingFunction="ease">
        {
          (styles) => (
            <>
              <Paper
                style={{
                  ...styles,
                  position: 'absolute',
                  bottom: '5rem',
                  right: '1rem',
                  width: '20vw',
                  textAlign: 'center',
                }}
                component="div"
                shadow="md"
                padding="md"
                withBorder
                className="floating-action-button-menu"
                ref={clickOutsideRef}
              >
                <Link to="/insert">
                  <Text className="menu-text" weight={600}>
                    Add item
                  </Text>
                </Link>
                <Divider color="#b1b1b1" />
                <Link to="/create/outfit">
                  <Text className="menu-text" weight={600}>
                    Create outfit
                  </Text>
                </Link>
              </Paper>
              <div className="blur" />
            </>
          )
        }
      </Transition>
    </>
  );
};

export default FloatingActionButton;

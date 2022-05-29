import "./DragAndDropZone.scss";
import React, { useState } from "react";
import { useNavigate } from "react-router-dom";

import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faImage, faXmark, faArrowUpFromBracket } from "@fortawesome/free-solid-svg-icons";
import { Group, Text } from "@mantine/core";
import { Dropzone, IMAGE_MIME_TYPE } from "@mantine/dropzone";

import clothesService from "../../services/Clothes";

function getIcon(status) {
  if (status.accepted) return faArrowUpFromBracket;
  else if (status.rejected) return faXmark;
  return faImage;
}

// FIXME status not updating correctly
function dropzoneChildren(status) {
  return (
    <Group position="center" spacing="xl" style={{ minHeight: 220 }}>
      <FontAwesomeIcon icon={getIcon(status)} size="5x" />
      <div>
        <Text size="xl" inline>
          Drag an image here or click to select a file
        </Text>
        <Text size="sm" color="dimmed" inline mt={7}>
          Attach only a file at the time!
        </Text>
      </div>
    </Group>
  )
}

function DragAndDropZone(props) {
  const [isLoading, load] = useState(false);
  const navigate = useNavigate();

  let { width } = props;
  width = !width ? "100%" : width

  // TODO make call to back to upload file
  // https://stackoverflow.com/questions/72109545/mantine-dropzone-react-image-upload-issues-while-image-upload-on-login-form
  // Remember to use params to send file URL for the next page
  function loadImages(files) {
    load(true);
    const formData = new FormData();
    formData.append('file', files[0]);
    clothesService.createClothes('', files[0], [])
    // setTimeout(() => navigate('/insert/product'), 1000);
  }

  return (
    <div className="drag-and-drop-zone" style={{ width: width }}>
      <Dropzone
        onDrop={(files) => loadImages(files)}
        onReject={(files) => console.log('rejected files', files)}
        maxSize={3 * 1024 ** 2}
        accept={IMAGE_MIME_TYPE}
        loading={isLoading}
        multiple={false}
      >
        {(status) => dropzoneChildren(status)}
      </Dropzone>
    </div>
  );
};

export default DragAndDropZone;

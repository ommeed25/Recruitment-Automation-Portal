import { useEffect, useState } from "react";
import "./VendorPartnership.css";

import {
  getVendorSettings,
  getVendorImages,
  getVendorHashtags,
  selectVendorImage,
  uploadVendorImage,
  deleteVendorImage,
  addVendorHashtags,
  deleteVendorHashtag,
  updateVendorSettings,
} from "../services/vendor";

export default function VendorPartnership() {
  const [settings, setSettings] = useState(null);
  const [images, setImages] = useState([]);
  const [hashtags, setHashtags] = useState([]);
  const [selectedFile, setSelectedFile] = useState(null);
  const [newHashtags, setNewHashtags] = useState("");

  useEffect(() => {
    const loadVendorData = async () => {
      try {
        const [settingsData, imagesData, hashtagsData] = await Promise.all([
          getVendorSettings(),
          getVendorImages(),
          getVendorHashtags(),
        ]);

        setSettings(settingsData);
        setImages(imagesData);
        setHashtags(hashtagsData);
      } catch (error) {
        console.error("Failed to load vendor data:", error);
      }
    };

    void loadVendorData();
  }, []);

  const handleSelectImage = async (imageId) => {
    try {
      await selectVendorImage(imageId);

      const updatedImages = await getVendorImages();
      const updatedSettings = await getVendorSettings();

      setImages(updatedImages);
      setSettings(updatedSettings);
    } catch (error) {
      console.error("Failed to select vendor image:", error);
      alert("Unable to select image");
    }
  };

  const handleUpload = async () => {
    if (!selectedFile) {
      return;
    }

    try {
      await uploadVendorImage(selectedFile);

      setSelectedFile(null);

      const updatedImages = await getVendorImages();
      setImages(updatedImages);
    } catch (error) {
      console.error("Failed to upload vendor image:", error);
      alert("Unable to upload image");
    }
  };

  const handleDeleteImage = async (imageId, filename) => {
    if (
      !window.confirm(
        `Delete "${filename}"?\n\nThis image will be permanently removed.`,
      )
    ) {
      return;
    }

    try {
      await deleteVendorImage(imageId);

      const updatedImages = await getVendorImages();
      setImages(updatedImages);
    } catch (error) {
      console.error("Failed to delete vendor image:", error);

      alert(error.response?.data?.detail || "Unable to delete image");
    }
  };

  const handleAddHashtags = async () => {
    const parsedHashtags = newHashtags
      .split("#")
      .map((tag) => tag.trim())
      .filter(Boolean)
      .map((tag) => `#${tag.replace(/^#+/, "")}`);

    if (parsedHashtags.length === 0) {
      return;
    }

    // Remove duplicates from what the user pasted
    const uniqueHashtags = [...new Set(parsedHashtags)];

    if (hashtags.length + uniqueHashtags.length > 30) {
      alert("Maximum 30 hashtags allowed.");
      return;
    }

    try {
      await addVendorHashtags(uniqueHashtags);

      const updatedHashtags = await getVendorHashtags();

      setHashtags(updatedHashtags);
      setNewHashtags("");
    } catch (error) {
      console.error("Failed to add hashtags:", error);

      alert(error.response?.data?.detail || "Unable to add hashtags");
    }
  };

  const handleDeleteHashtag = async (hashtagId, hashtag) => {
    if (!window.confirm(`Remove ${hashtag}?`)) {
      return;
    }

    try {
      await deleteVendorHashtag(hashtagId);

      const updatedHashtags = await getVendorHashtags();
      setHashtags(updatedHashtags);
    } catch (error) {
      console.error("Failed to delete hashtag:", error);

      alert(error.response?.data?.detail || "Unable to delete hashtag");
    }
  };

  const handleSaveSettings = async () => {
    if (!settings) {
      return;
    }

    try {
      const updatedSettings = await updateVendorSettings(
        settings.is_enabled,
        settings.posting_time,
      );

      setSettings(updatedSettings);

      alert("Vendor settings saved successfully");
    } catch (error) {
      console.error("Failed to save vendor settings:", error);
      alert("Unable to save vendor settings");
    }
  };

  return (
    <div className="vendor-page">
      <div className="vendor-header">
        <div>
          <h1>Vendor Partnership</h1>
          <p>Manage the image, hashtags, and daily LinkedIn posting.</p>
        </div>
      </div>

      <div className="vendor-card">
        <h2>Daily Posting</h2>

        <div className="vendor-setting-row">
          <span>Enable Daily Posting</span>

          <label className="switch">
            <input
              type="checkbox"
              checked={settings?.is_enabled ?? false}
              onChange={(e) =>
                setSettings((prev) => ({
                  ...prev,
                  is_enabled: e.target.checked,
                }))
              }
            />
            <span className="slider"></span>
          </label>
        </div>

        <div className="vendor-setting-row">
          <span>Posting Time</span>

          <input
            type="time"
            value={settings?.posting_time ?? "10:00"}
            onChange={(e) =>
              setSettings((prev) => ({
                ...prev,
                posting_time: e.target.value,
              }))
            }
          />
        </div>
      </div>

      <div className="vendor-card">
        <h2>Vendor Image</h2>

        <p className="vendor-muted">
          Select the image that will be posted every morning.
        </p>

        <input
          type="file"
          id="vendor-image-upload"
          accept="image/png,image/jpeg,image/webp"
          hidden
          onChange={(e) => {
            const file = e.target.files?.[0];

            if (!file) {
              return;
            }

            setSelectedFile(file);
          }}
        />

        <div className="vendor-image-section">
          <div className="vendor-image-preview">
            {images.find((image) => image.is_active) ? (
              <>
                <img
                  src={`/${images.find((image) => image.is_active).file_path}`}
                  alt={images.find((image) => image.is_active).filename}
                />
                <div className="vendor-image-preview-label">
                  Active Image Preview
                </div>
              </>
            ) : (
              <div className="vendor-image-preview-empty">
                No active image selected. Click a thumbnail on the right to
                choose one.
              </div>
            )}
          </div>

          <div className="vendor-image-controls">
            <div className="vendor-image-actions">
              <label
                htmlFor="vendor-image-upload"
                className="vendor-upload-btn"
              >
                + Choose Image
              </label>

              {selectedFile && (
                <span className="vendor-selected-file">
                  Selected file: {selectedFile.name}
                </span>
              )}

              <button
                type="button"
                className="vendor-image-upload-btn"
                onClick={handleUpload}
                disabled={!selectedFile}
              >
                Upload Image
              </button>
            </div>

            <p className="vendor-image-help">
              Upload JPG, PNG, or WEBP. Once uploaded, click a thumbnail to make
              it active.
            </p>

            <div className="vendor-images">
              {images.length === 0 ? (
                <div className="vendor-empty">
                  No vendor images uploaded yet.
                </div>
              ) : (
                images.map((image) => (
                  <div
                    key={image.id}
                    className={`vendor-image-card ${
                      image.is_active ? "active" : ""
                    }`}
                    onClick={() => handleSelectImage(image.id)}
                  >
                    <button
                      type="button"
                      className="vendor-image-delete"
                      onClick={(e) => {
                        e.stopPropagation();

                        handleDeleteImage(image.id, image.filename);
                      }}
                    >
                      ×
                    </button>

                    <img
                      src={`/${image.file_path}`}
                      alt={image.filename}
                    />

                    <div className="vendor-image-info">
                      <div className="vendor-image-name">{image.filename}</div>

                      {image.is_active && (
                        <span className="vendor-image-status">Active</span>
                      )}
                    </div>
                  </div>
                ))
              )}
            </div>
          </div>
        </div>
      </div>

      <div className="vendor-card">
        <div className="vendor-card-header">
          <div>
            <h2>Hashtags</h2>
            <p className="vendor-muted">
              Add up to 30 hashtags for the daily post.
            </p>
          </div>

          <span className="hashtag-count">{hashtags.length} / 30</span>
        </div>

        <div className="hashtag-list">
          {hashtags.length === 0 ? (
            <div className="vendor-empty">No hashtags added yet.</div>
          ) : (
            hashtags.map((item) => (
              <div key={item.id} className="hashtag-item">
                {item.hashtag}

                <button
                  className="hashtag-delete"
                  type="button"
                  onClick={() => handleDeleteHashtag(item.id, item.hashtag)}
                >
                  ×
                </button>
              </div>
            ))
          )}
        </div>

        <div className="hashtag-add">
          <textarea
            placeholder="Paste hashtags separated by #"
            value={newHashtags}
            onChange={(e) => setNewHashtags(e.target.value)}
            rows={4}
          />

          <button
            type="button"
            onClick={handleAddHashtags}
            disabled={hashtags.length >= 30}
          >
            Add
          </button>
        </div>
      </div>

      <div className="vendor-actions">
        <button
          className="save-vendor-btn"
          type="button"
          onClick={handleSaveSettings}
        >
          Save Settings
        </button>
      </div>
    </div>
  );
}

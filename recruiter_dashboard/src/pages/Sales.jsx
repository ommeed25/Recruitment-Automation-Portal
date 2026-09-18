import { useEffect, useState } from "react";
import "./VendorPartnership.css";

import {
  getSalesSettings,
  updateSalesSettings,
  getSalesImages,
  uploadSalesImage,
  selectSalesImage,
  deleteSalesImage,
  getSalesHashtags,
  addSalesHashtags,
  deleteSalesHashtag,
} from "../services/sales";

function parseHashtags(value) {
  const uniqueHashtags = new Map();

  value
    .split(/[\s,]+/)
    .map((tag) => tag.replace(/^#+/, "").trim())
    .filter(Boolean)
    .forEach((tag) => {
      const hashtag = `#${tag}`;
      const normalized = hashtag.toLowerCase();

      if (!uniqueHashtags.has(normalized)) {
        uniqueHashtags.set(normalized, hashtag);
      }
    });

  return [...uniqueHashtags.values()];
}

export default function Sales() {
  const [settings, setSettings] = useState(null);
  const [images, setImages] = useState([]);
  const [hashtags, setHashtags] = useState([]);
  const [selectedFile, setSelectedFile] = useState(null);
  const [newHashtags, setNewHashtags] = useState("");
  const [selectedHashtagIds, setSelectedHashtagIds] = useState([]);

  useEffect(() => {
    const loadData = async () => {
      try {
        const [settingsData, imagesData, hashtagsData] =
          await Promise.all([
            getSalesSettings(),
            getSalesImages(),
            getSalesHashtags(),
          ]);

        setSettings(settingsData);
        setImages(imagesData);
        setHashtags(hashtagsData);
      } catch (error) {
        console.error("Failed to load Sales data:", error);
      }
    };

    void loadData();
  }, []);

  const handleSelectImage = async (imageId) => {
    try {
      await selectSalesImage(imageId);

      const [updatedImages, updatedSettings] = await Promise.all([
        getSalesImages(),
        getSalesSettings(),
      ]);

      setImages(updatedImages);
      setSettings(updatedSettings);
    } catch (error) {
      console.error("Failed to select Sales image:", error);
      alert("Unable to select image");
    }
  };

  const handleUpload = async () => {
    if (!selectedFile) return;

    try {
      await uploadSalesImage(selectedFile);

      setSelectedFile(null);

      const updatedImages = await getSalesImages();
      setImages(updatedImages);
    } catch (error) {
      console.error("Failed to upload Sales image:", error);
      alert("Unable to upload image");
    }
  };

  const handleDeleteImage = async (imageId, filename) => {
    if (
      !window.confirm(
        `Delete "${filename}"?\n\nThis image will be permanently removed.`
      )
    ) {
      return;
    }

    try {
      await deleteSalesImage(imageId);

      const updatedImages = await getSalesImages();
      setImages(updatedImages);
    } catch (error) {
      console.error("Failed to delete Sales image:", error);
      alert(
        error.response?.data?.detail || "Unable to delete image"
      );
    }
  };

  const handleAddHashtags = async () => {
    const parsed = parseHashtags(newHashtags);

    if (parsed.length === 0) return;

    const existing = new Set(
      hashtags.map((item) => item.hashtag.toLowerCase())
    );

    const unique = parsed.filter(
      (hashtag) => !existing.has(hashtag.toLowerCase())
    );

    if (unique.length === 0) {
      setNewHashtags("");
      return;
    }

    if (hashtags.length + unique.length > 30) {
      alert("Maximum 30 hashtags allowed.");
      return;
    }

    try {
      await addSalesHashtags(unique);

      const updated = await getSalesHashtags();

      setHashtags(updated);
      setNewHashtags("");
    } catch (error) {
      console.error("Failed to add Sales hashtags:", error);
      alert(
        error.response?.data?.detail ||
          "Unable to add hashtags"
      );
    }
  };

  const handleDeleteHashtag = async (hashtagId, hashtag) => {
    if (!window.confirm(`Remove ${hashtag}?`)) return;

    try {
      await deleteSalesHashtag(hashtagId);

      const updated = await getSalesHashtags();

      setHashtags(updated);
      setSelectedHashtagIds((current) =>
        current.filter((id) => id !== hashtagId)
      );
    } catch (error) {
      console.error("Failed to delete Sales hashtag:", error);
      alert(
        error.response?.data?.detail ||
          "Unable to delete hashtag"
      );
    }
  };

  const handleToggleHashtag = (hashtagId) => {
    setSelectedHashtagIds((current) =>
      current.includes(hashtagId)
        ? current.filter((id) => id !== hashtagId)
        : [...current, hashtagId]
    );
  };

  const handleToggleAll = () => {
    setSelectedHashtagIds((current) =>
      current.length === hashtags.length
        ? []
        : hashtags.map((item) => item.id)
    );
  };

  const handleDeleteSelected = async () => {
    if (selectedHashtagIds.length === 0) return;

    try {
      await Promise.all(
        selectedHashtagIds.map((id) => deleteSalesHashtag(id))
      );

      setHashtags(await getSalesHashtags());
      setSelectedHashtagIds([]);
    } catch (error) {
      console.error("Failed to delete selected Sales hashtags:", error);
      alert("Unable to delete selected hashtags");
    }
  };

  const handleDeleteAll = async () => {
    if (
      hashtags.length === 0 ||
      !window.confirm("Delete all hashtags?")
    ) {
      return;
    }

    try {
      await Promise.all(
        hashtags.map((item) => deleteSalesHashtag(item.id))
      );

      setHashtags(await getSalesHashtags());
      setSelectedHashtagIds([]);
    } catch (error) {
      console.error("Failed to delete Sales hashtags:", error);
      alert("Unable to delete all hashtags");
    }
  };

  const handleSaveSettings = async () => {
    if (!settings) return;

    try {
      const updated = await updateSalesSettings(
        settings.is_enabled,
        settings.posting_time
      );

      setSettings(updated);
      alert("Sales settings saved successfully");
    } catch (error) {
      console.error("Failed to save Sales settings:", error);
      alert("Unable to save Sales settings");
    }
  };

  const activeImage = images.find((image) => image.is_active);

  return (
    <div className="vendor-page">
      <div className="vendor-header">
        <div>
          <h1>Sales</h1>
          <p>
            Manage Sales images, hashtags, and daily LinkedIn posting.
          </p>
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
        <h2>Sales Image</h2>

        <p className="vendor-muted">
          Select the image that will be used for Sales posts.
        </p>

        <input
          type="file"
          id="sales-image-upload"
          accept="image/png,image/jpeg,image/webp"
          hidden
          onChange={(e) =>
            setSelectedFile(e.target.files?.[0] || null)
          }
        />

        <div className="vendor-image-section">
          <div className="vendor-image-preview">
            {activeImage ? (
              <>
                <img
                  src={activeImage.file_path}
                  alt={activeImage.filename}
                />
                <div className="vendor-image-preview-label">
                  Active Image Preview
                </div>
              </>
            ) : (
              <div className="vendor-image-preview-empty">
                No active image selected.
              </div>
            )}
          </div>

          <div className="vendor-image-controls">
            <div className="vendor-image-actions">
              <label
                htmlFor="sales-image-upload"
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
              Upload JPG, PNG, or WEBP. Click a thumbnail to make it
              active.
            </p>

            <div className="vendor-images">
              {images.length === 0 ? (
                <div className="vendor-empty">
                  No Sales images uploaded yet.
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
                        handleDeleteImage(
                          image.id,
                          image.filename
                        );
                      }}
                    >
                      ×
                    </button>

                    <img
                      src={image.file_path}
                      alt={image.filename}
                    />

                    <div className="vendor-image-info">
                      <div className="vendor-image-name">
                        {image.filename}
                      </div>

                      {image.is_active && (
                        <span className="vendor-image-status">
                          Active
                        </span>
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
              Add up to 30 hashtags for Sales posts.
            </p>
          </div>

          <span className="hashtag-count">
            {hashtags.length} / 30
          </span>
        </div>

        {hashtags.length > 0 && (
          <div className="hashtag-toolbar">
            <button
              type="button"
              className="hashtag-toolbar-btn"
              onClick={handleToggleAll}
            >
              {selectedHashtagIds.length === hashtags.length
                ? "Deselect All"
                : "Select All"}
            </button>

            <button
              type="button"
              className="hashtag-toolbar-btn hashtag-toolbar-btn-danger"
              onClick={handleDeleteSelected}
              disabled={selectedHashtagIds.length === 0}
            >
              Delete Selected
            </button>

            <button
              type="button"
              className="hashtag-toolbar-btn hashtag-toolbar-btn-danger"
              onClick={handleDeleteAll}
            >
              Delete All
            </button>
          </div>
        )}

        <div className="hashtag-list">
          {hashtags.length === 0 ? (
            <div className="vendor-empty">
              No hashtags added yet.
            </div>
          ) : (
            hashtags.map((item) => (
              <div
                key={item.id}
                className={`hashtag-item ${
                  selectedHashtagIds.includes(item.id)
                    ? "selected"
                    : ""
                }`}
              >
                <label className="hashtag-selection">
                  <input
                    type="checkbox"
                    checked={selectedHashtagIds.includes(item.id)}
                    onChange={() =>
                      handleToggleHashtag(item.id)
                    }
                  />
                  <span>{item.hashtag}</span>
                </label>

                <button
                  className="hashtag-delete"
                  type="button"
                  onClick={() =>
                    handleDeleteHashtag(
                      item.id,
                      item.hashtag
                    )
                  }
                >
                  ×
                </button>
              </div>
            ))
          )}
        </div>

        <div className="hashtag-add">
          <textarea
            placeholder="Add hashtags separated by commas, spaces, or new lines"
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
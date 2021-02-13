'use strict'

const downloadVideo = (videoId, iTag) => {
  downloadFile({videoId, iTag});
};

const downloadCaption = (videoId, captionCode) => {
  downloadFile({videoId, captionCode, isCaption: true});
};

const downloadFile = async (params) => {
  startLoadingIcon(params.iTag || params.captionCode);
  const response = await axios.post('/request_download', params);
  const link = response.data;
  $('a#download_link').attr({href: link});
  document.getElementById('download_link').click();
  stopLoadingIcon(params.iTag || params.captionCode);
};

const startLoadingIcon = (buttonId) => {
  $(`button#${buttonId}>span:first-child`).css('display', '');
  $('button.download-button').prop('disabled', true);
};

const stopLoadingIcon = (buttonId) => {
  $(`button#${buttonId}>span:first-child`).css('display', 'none');
  $('button.download-button').prop('disabled', false);
};

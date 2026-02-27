$(function () {
  const $main = $('.js-slider-main');
  const $nav = $('.js-slider-nav');

  $main.slick({
    arrows: false,
    slidesToShow: 1,
    slidesToScroll: 1,
    asNavFor: '.js-slider-nav',
    adaptiveHeight: true,
  });

  $nav.slick({
    arrows: true,
    slidesToShow: 4,
    slidesToScroll: 1,
    asNavFor: '.js-slider-main',
    focusOnSelect: true,
    infinite: true,
    responsive: [
      {
        breakpoint: 992,
        settings: { slidesToShow: 3 },
      },
      {
        breakpoint: 576,
        settings: { slidesToShow: 2 },
      },
    ],
  });

  const lightbox = GLightbox({
    selector: '.glightbox',
    loop: true,
  });

  $('.slide-open-btn').on('click', function () {
    const index = Number($(this).data('index'));
    lightbox.openAt(index);
  });
});

$(function () {
  const $main = $('.js-slider-main');
  const $nav = $('.js-slider-nav');

  if (!$main.length || !$nav.length) {
    return;
  }

  $main.slick({
    arrows: false,
    slidesToShow: 1,
    slidesToScroll: 1,
    asNavFor: '.js-slider-nav',
    adaptiveHeight: true,
    infinite: $main.children().length > 1,
  });

  $nav.slick({
    arrows: true,
    slidesToShow: 4,
    slidesToScroll: 1,
    asNavFor: '.js-slider-main',
    focusOnSelect: true,
    infinite: $nav.children().length > 4,
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

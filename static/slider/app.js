$(function () {
  const $main = $('.js-slider-main');
  const $nav = $('.js-slider-nav');

  if (!$main.length || !$nav.length) {
    return;
  }

  const slidesCount = $main.children().length;

  $main.slick({
    arrows: false,
    slidesToShow: 1,
    slidesToScroll: 1,
    asNavFor: '.js-slider-nav',
    adaptiveHeight: true,
    infinite: slidesCount > 1,
  });

  $nav.slick({
    arrows: false,
    slidesToShow: 5,
    slidesToScroll: 1,
    asNavFor: '.js-slider-main',
    focusOnSelect: true,
    infinite: slidesCount > 5,
    responsive: [
      {
        breakpoint: 992,
        settings: { slidesToShow: 4 },
      },
      {
        breakpoint: 576,
        settings: { slidesToShow: 5 },
      },
    ],
  });

  $('.js-main-prev').on('click', function () {
    $main.slick('slickPrev');
  });

  $('.js-main-next').on('click', function () {
    $main.slick('slickNext');
  });

  if (slidesCount < 2) {
    $('.slider-control').hide();
  }

  const lightbox = GLightbox({
    selector: '.glightbox',
    loop: true,
  });

  $('.slide-open-btn').on('click', function () {
    const index = Number($(this).data('index'));
    lightbox.openAt(index);
  });
});

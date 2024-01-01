class UIConstants:
    fontSizeRegular = 0.03
    fontSizeTitle = 0.04
    fontSizeHeader = 0.05
    fontSizeDetail = 0.025

    headerFooterHeight = 0.08

    clockWidth = 0.22
    clockPadding = 0.01

    panelWidth = 0.7
    panelPadding = 0.03
    panelBorderWidth = 0.005
    panelHeaderHeight = 0.08
    panelContentWidth = panelWidth - (panelPadding * 2)
    panelInputHeight = 0.06
    panelValidationHeight = 0.04
    panelTitleHeight = 0.08
    panelTextHeight = 0.04
    panelScrollbarPadding = panelPadding / 2

    inputPaddingVertical = 0.3
    inputPaddingHorizontal = 0.1
    inputUnderlineHeight = 0.005

    panelSliderWidth = panelContentWidth * 0.66
    sliderHeight = 0.03
    sliderHandleWidth = 0.005
    sliderHandleHeight = 0.02

    checkboxSize = 0.04
    checkboxPadding = 0.015

    scrollbarWidth = 0.01

    animationSliderWidth = 0.6
    animationSliderPadding = headerFooterHeight / 2
    animationButtonWidth = headerFooterHeight
    animationButtonGroupWidth = 3 * animationButtonWidth
    animationControlsWidth = (
        animationSliderWidth
        + 2 * animationSliderPadding
        + 2 * animationButtonGroupWidth
    )

    legendPadding = 0.015
    legendLabelWidth = 0.8
    legendLabelHeight = 0.05
    legendScaleWidth = 0.15
    legendScaleHeight = 1
    legendScaleBarWidth = 0.03
    legendTitleHeight = 0.06
    legendScaleBarHeight = legendScaleHeight - 4 * legendPadding - legendTitleHeight

    modalPadding = 0.05
    modalTitleHeight = 0.08
    modalScrollbarPadding = modalPadding / 2

    modalFooterButtonWidth = 0.2
    modalFooterButtonHeight = 0.05

    addressModalWidth = 0.7
    addressModalSearchbarHeight = 0.05

    # Higher number means slower scrolling
    scrollSensitivity = 10

    # This is way bigger than the screen could ever be
    infinity = 1000

class UIConstants:
    fontSizeRegular = 0.03
    fontSizeTitle = 0.04
    fontSizeHeader = 0.05
    fontSizeDetail = 0.025

    headerFooterHeight = 0.08

    clockWidth = 0.22
    clockPadding = 0.01

    headerButtonWidth = headerFooterHeight * 1.6

    badgeSize = 0.03

    panelWidth = 0.7
    panelPadding = 0.03
    panelBorderWidth = 0.005
    panelHeaderHeight = 0.08
    panelContentWidth = panelWidth - (panelPadding * 2)
    panelInputHeight = 0.06
    panelValidationHeight = 0.04
    panelTitleHeight = 0.08
    panelScrollbarPadding = panelPadding / 2
    panelButtonGroupHeight = 0.04

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

    markerItemPadding = 0.015
    markerItemButtonSize = 0.06
    markerItemTextWidth = (
        panelContentWidth - (4 * markerItemPadding) - (2 * markerItemButtonSize)
    )
    markerItemTextLeft = (2 * markerItemPadding) + markerItemButtonSize
    markerItemMinHeight = markerItemButtonSize + (2 * markerItemPadding)

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

    mapMarkerSize = 0.07

    modalPadding = 0.05
    modalTitleHeight = 0.08
    modalScrollbarPadding = modalPadding / 2

    modalFooterButtonWidth = 0.2
    modalFooterButtonHeight = 0.05

    addressModalWidth = 0.7
    addressModalSearchbarHeight = 0.05
    addressModalResultButtonsMaxHeight = 0.3
    addressModalResultButtonTextPadding = 0.015
    addressModalResultButtonPadding = 0.01
    addressModalResultButtonHeight = 0.05
    addressModalResultButtonHeightDouble = 0.09

    licenseModalWidth = 1.2
    licenseModalHeight = 0.8

    alertsModalWidth = 0.8
    alertsModalHeight = 0.8

    alertsButtonHeight = 0.09
    alertsButtonPadding = 0.01
    alertsButtonTextLeftPadding = 0.025
    alertsButtonTextVerticalPadding = 0.003
    alertsButtonBorderWidth = 0.01
    alertsButtonTextRightPadding = alertsButtonTextLeftPadding - alertsButtonBorderWidth

    alertModalWidth = 1.2
    alertModalMaxHeight = 1.0

    labelPadding = 0.01

    # Higher number means slower scrolling
    scrollSensitivity = 10

    # This is way bigger than the screen could ever be
    infinity = 1000

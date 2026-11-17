#include QMK_KEYBOARD_H

enum layers {
    _BASE
};

const uint16_t PROGMEM keymaps[][MATRIX_ROWS][MATRIX_COLS] = {

    [_BASE] = LAYOUT_3x4(
        KC_F1,   KC_F2,   KC_F3,   KC_F4,
        KC_F5,   KC_UP,   KC_F6,   KC_F7,
        KC_LEFT, KC_DOWN, KC_RGHT, KC_ESC
    )

};
int calc_sweep_index(float el) {
    int l = 0;
    int r = scan_count[0];

    for (int i = 0; i < 20; i++) {
        int m = (l + r) / 2;

        if (el < elevation[m]) {
            r = m;
        } else {
            l = m;
        }

        if (r - l <= 1) {
            return l;
        }
    }

    return 0;
}

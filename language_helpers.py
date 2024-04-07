def get_EXPECTED_IC(language):
    IC_english = 0.0667
    IC_portuguese = 0.0745
    return IC_english if language == "english" else IC_portuguese


english_frequency: dict[str, float] = dict(a=8.167, b=1.492, c=2.782, d=4.253, e=12.702, f=2.228, g=2.015, h=6.094, i=6.966, j=0.153,
                         k=0.772, l=4.025, m=2.406, n=6.749, o=7.507, p=1.929, q=0.095, r=5.987, s=6.327, t=9.056,
                         u=2.758, v=0.978, w=2.360, x=0.150, y=1.974, z=0.074)

portuguese_frequency: dict[str, float] = dict(a=14.63, b=1.04, c=3.88, d=4.99, e=12.57, f=1.02, g=1.30, h=1.28, i=6.18, j=0.40, k=0.02,
                            l=2.78, m=4.74, n=5.05, o=10.73, p=2.52, q=1.20, r=6.53, s=7.81, t=4.34, u=4.63, v=1.67,
                            w=0.01, x=0.21, y=0.01, z=0.47)

alphabetsFrequencies: dict[str, dict[str, float]] = dict(portuguese=portuguese_frequency, english=english_frequency)

english_frequency_top10: dict[str, float] = dict(E=12.702, T=9.056, A=8.167, O=7.507, I=6.966, N=6.749, S=6.327, H=6.094, R=5.987,
                               D=4.253)

portuguese_frequency_top10: dict[str, float] = dict(A=14.63, E=12.57, O=10.73, S=7.81, R=6.53, I=6.18, N=5.05, D=4.99, M=4.74, U=4.63)

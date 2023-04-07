#pragma once

#ifdef COLORDETECTION_EXPORTS
#define COLORDETECTION_API __declspec(dllexport)
#else
#define COLORDETECTION_API __declspec(dllimport)
#endif

extern "C"
{
    COLORDETECTION_API void DetectColors(unsigned char* input, int width, int height, int channels, float* lowerHSV, float* upperHSV, int* numContours);
}

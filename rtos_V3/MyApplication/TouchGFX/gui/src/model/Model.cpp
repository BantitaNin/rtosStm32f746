#include <gui/model/Model.hpp>
#include <gui/model/ModelListener.hpp>
#include <cstring>

extern Model model;
Model model;

extern "C" void SetPredictionLabel(const char* label)
{
    model.setPredictionLabel(label);
}

Model::Model() : modelListener(0)
{

}

void Model::tick()
{
}

void Model::setPredictionLabel(const char* newLabel)
{
    strncpy(predictionLabel, newLabel, sizeof(predictionLabel) - 1);
    predictionLabel[sizeof(predictionLabel) - 1] = '\0';
}

const char* Model::getPredictionLabel() const
{
    return predictionLabel;
}

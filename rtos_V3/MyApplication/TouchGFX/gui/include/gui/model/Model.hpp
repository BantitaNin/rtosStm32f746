#ifndef MODEL_HPP
#define MODEL_HPP

class ModelListener;

class Model
{
public:
    Model();

    void bind(ModelListener* listener)
    {
        modelListener = listener;
    }

    void tick();

    void setPredictionLabel(const char* newLabel);
        const char* getPredictionLabel() const;
protected:
    ModelListener* modelListener;
private:
    char predictionLabel[20];
};

#endif // MODEL_HPP
